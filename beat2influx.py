#!/usr/bin/python3
"""
Logs Beat Saber song and performance metrics to influxdb
"""
import asyncio
import json
import logging
import os
import time

import influxdb
import websockets
from dotenv import load_dotenv
from influxdb.exceptions import InfluxDBClientError
from pydantic import ValidationError
from websockets.exceptions import ConnectionClosedError

from models import *

load_dotenv()  # take environment variables from .env.

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

BEATSABER_SOCKET = os.getenv("BEATSABER_SOCKET", "ws://localhost:6557/socket")
INFLUX_HOST = os.getenv("INFLUX_HOST", "localhost")
INFLUX_DB = os.getenv("INFLUX_DB", "beat2influx")
INFLUX_USER = os.getenv("INFLUX_USER", "admin")
INFLUX_PASS = os.getenv("INFLUX_PASS", "admin")
CONNECTED_COMMAND = os.getenv("CONNECTED_COMMAND", None)  # Command to execute after client has connected to Beat Saber

LOG_RESPONSES = False
song_start_data = None
last_song_name = None


def connect_db():
    client = influxdb.InfluxDBClient(
        host=INFLUX_HOST,
        username=INFLUX_USER,
        password=INFLUX_PASS,
        database=INFLUX_DB
    )
    client.create_database(INFLUX_DB)
    return client


async def save_start(status):
    global song_start_data
    global last_song_name
    logger.info("Level started")

    if 'beatmap' not in status:
        return

    song_start_data = []

    try:
        beatmap = Beatmap.parse_obj(status['beatmap'])
        last_song_name = beatmap.songName
        song_start_data.append({
            "measurement": 'beatmap',
            "fields": beatmap.dict()
        })
    except ValidationError as err:
        logger.error(f"Beatmap validation error {err}")

    if status['mod'] != 'null':
        try:
            mod = Mod.parse_obj(status['mod'])

            song_start_data.append({
                "measurement": 'mods',
                "tags": {
                    "songName": last_song_name
                },
                "fields": mod.dict()
            })
        except ValidationError as err:
            logger.error(f"Mod validation error {err}")


def write_to_db(query, db):
    try:
        db.write_points(query)
    except InfluxDBClientError as error:
        logger.error(f"Error writing to db {error}")


async def log_done(status, db):
    global song_start_data
    logger.error("Level finished")
    if 'performance' not in status:
        logger.error("Performance data missing")
        return
    if song_start_data is None:
        logger.error("Log done without start data!")
        song_start_data = []
    try:
        performance = Performance.parse_obj(status['performance'])
        song_start_data.append({
            "measurement": 'performance',
            "tags": {
                "songName": last_song_name
            },
            "fields": performance.dict()
        })
    except ValidationError as err:
        logger.error(f"Performance validation error {err}")

    logger.debug(song_start_data)

    write_to_db(song_start_data, db)

    song_start_data = None


async def log_note(event, db, miss=False):
    logger.debug("Log Note")
    if 'noteCut' not in event:
        return
    if event['noteCut'] == 'null':
        return

    measurement = "noteMiss" if miss else "noteCut"
    cut_event = NoteCut.parse_obj(event['noteCut'])

    query = [{
        "measurement": measurement,
        "tags": {
            "songName": last_song_name
        },
        "fields": cut_event.dict()
    }]

    write_to_db(query, db)


def log_response(message):
    with open('log.json', 'a') as logfile:
        logfile.write(message + "\n")
        logfile.close()


async def callback(message, db):
    event = json.loads(message)
    if LOG_RESPONSES:
        log_response(message)

    event_type = event['event']
    logger.debug(f"Event Type: {event_type}")

    if event_type == 'songStart':
        await save_start(event['status'])
    elif event_type == 'finished' or event_type == 'failed':
        await log_done(event['status'], db)
    elif event_type == 'noteFullyCut' or event_type == 'noteCut':
        await log_note(event, db, miss=False)
    elif event_type == 'noteMissed':
        await log_note(event, db, miss=True)
    elif event_type == 'hello':
        logger.error("Received hello vom Beat Saber!")
        if CONNECTED_COMMAND is not None:
            os.system(CONNECTED_COMMAND)


async def consumer_handler():
    try:
        async with websockets.connect(BEATSABER_SOCKET, max_size=None) as websocket:
            db = connect_db()
            logger.info("Connected")
            async for message in websocket:
                try:
                    await callback(message, db)
                except InfluxDBClientError as e:
                    log_response(f"{e}\n{message}")
            db.close()
    except (ConnectionRefusedError, OSError) as e:
        logger.debug(f"Could not connect {e}")
    except ConnectionClosedError as e:
        logger.info(f"Disconnected: {e}")


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    while True:
        try:
            event_loop.run_until_complete(consumer_handler())
            logger.info("Waiting for connection")

            time.sleep(10)
        except KeyboardInterrupt:
            event_loop.stop()
            break

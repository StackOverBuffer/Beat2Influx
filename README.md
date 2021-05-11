# Beat2Influx
Beat Saber Influxdb logger

Logs Beat Saber performance and song data to Influxdb. For logged values see `models.py`

## Installation
### Requirements
- [Beat Saber HTTP Status Plugin](https://github.com/opl-/beatsaber-http-status)
- Influxdb 1.8
- Python3
- (Grafana)
### Configuration
If you want to change the defaults create a .env file
```ini
BEATSABER_SOCKET=ws://localhost:6557/socket
INFLUX_HOST=localhost
INFLUX_DB=beat2influx
INFLUX_USER=admin
INFLUX_PASS=admin
```
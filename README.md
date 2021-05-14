# Beat2Influx
Beat Saber Influxdb logger

Log your Beat Saber performance and song data to Influxdb and build beautiful dashboards with Grafana.

For logged values see `models.py`

## Installation
### Requirements
- [Beat Saber HTTP Status Plugin](https://github.com/opl-/beatsaber-http-status)
- Influxdb 1.8
- Python3 (+ requirements.txt)
- (Grafana)
### Configuration
To change the default configuration create a .env file
```ini
BEATSABER_SOCKET=ws://localhost:6557/socket
INFLUX_HOST=localhost
INFLUX_DB=beat2influx
INFLUX_USER=admin
INFLUX_PASS=admin

#optional, in case you want to run a script after the client has connected to Beat Saber
CONNECTED_COMMAND=bash beep.sh
```
## Simple Web Javascript MQTT client for Tasmota devices

This is a simple web client-based MQTT-over-WebSockets client for 
[Tasmota](https://github.com/arendst/Tasmota) devices.  It utilizes
the paho-mqtt-ws websockets javascript MQTT client.  (Feel free to replace the
cloudfare hosted mqttws31.js with your own.)

### Requirements:
* MQTT-over-WS enabled on your MQTT Server
* "Power Retain" turned on in Tasmota (cmnd/Device/PowerRetain ON)

### Config:
There are three variables you can configure in config.js:
* HOST = "mqtt"  <- put the hostname of your MQTT server here
* PORT = 9001    <- put the port number of the MQTT-WEBSOCKET listener
* ignoreChar = "_" <- MQTT topics that start with this character will be ignored

### SimpleServer
Usage:  ```simpleserver.py PORT```
Launches a simple webserver on the port number of your choosing.

### Interfaces:
There are three web interfaces:
* / : the "switches" interface
* /rssi : Shows the current WiFi RSSI of all online devices
* /webint : Shows the name and IP address of all online devices
-----
![WebMQTT](https://cdn.phreakmonkey.com/misc/webmqtt-screenshot.png "WebMQTT Screenshot")
![RSSI](https://cdn.phreakmonkey.com/misc/webmqtt-rssi.png "RSSI Screenshot")
![webint](https://cdn.phreakmonkey.com/misc/webmqtt-webint.png "WebInt Screenshot")
-----

## Simple Web Javascript MQTT client for Sonoff Tasmota devices

This is a simple web client-based MQTT-over-WebSockets client for 
[Sonoff Tasmota](https://github.com/arendst/Tasmota) devices.  It utilizes
the paho-mqtt-ws websockets javascript MQTT client.  (Feel free to replace the
cloudfare hosted mqttws31.js with your own.)

### Requirements:
* MQTT-over-WS enabled on your MQTT Server
* "Power Retain" turned on in Tasmota (cmnd/Device/PowerRetain ON)

### Config:
There are three variables you can configure in webmqtt.html:
* HOST = "mqtt"  <- put the hostname of your MQTT server here
* PORT = 9001    <- put the port number of the MQTT-WEBSOCKET listener
* ignoreChar = "_" <- MQTT topics that start with this character will be ignored
-----
![WebMQTT](https://cdn.phreakmonkey.com/misc/webmqtt-screenshot.png "WebMQTT Screenshot")
-----

# gateway-ic

In this repository is the IC-gateway that I'm developing for the IntersCity platform.

It aims to intermediate the communication between real sensors and the platform, transforming mqtt/coap data into REST requests

Implementation:
- There is a simple mqtt ans COAP communication already implemented

Requirements
    -Python
     - requests
     - peewee
     - Paho-Mqtt
     - CoAPthon
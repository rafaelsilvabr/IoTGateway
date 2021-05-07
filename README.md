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

Padrao de dados

Dados registro REAL Sensor

	msg={'localId':LocalId,
	    'regInfos':{
		 'capabilities':["temperature"],
		 'description':'A simple test'},
	     'registred': False,
	     'estado': True}

Dados publiccao

	msg={'localId':LocalId,
	     'data':{"humidity":50,"temperature":40},
	     'registred': True,
	     'estado':True}

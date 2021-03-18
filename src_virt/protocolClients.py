import json
from abc import ABCMeta, abstractmethod
from registry import Registry
from sender import Sender
import timeit 

from virtualizer import Virtualizer

class ProtocolClient ():
	__metaclass__ = ABCMeta
	def __init__(self,gatewayId):
		self.gatewayId = gatewayId
		self.reg = Registry()
		self.send = Sender()
		self.virt = Virtualizer()

	@abstractmethod
	def dataProcessing(self):
		pass

#-----------------------------MQTT--------------------------------------------
import paho.mqtt.client as mqtt

class MqttClass (ProtocolClient):
	def __init__(self, gatewayId, mqttAddress, mqttPort, mqttTimeout, mqttTopic):
		ProtocolClient.__init__(self,gatewayId)
		self.mqttAddress = mqttAddress
		self.mqttPort = mqttPort
		self.mqttTimeout = mqttTimeout
		self.mqttTopic = mqttTopic

	def test(self,receivedData):
		print('test')

	def dataProcessing(self,client,receivedData):
		#check type of message, with ot without state
		print('dataProcessing Started')
		if(receivedData['estado']==True):
			print('Sensor with status identified')
			if(receivedData['registered']==False):
				dbIds = self.reg.registerResourceIC(receivedData['localId'],receivedData['regInfos'])
				if(dbIds != False):
					#send confirmation to client
					confirm={'registered':True
					}
					client.publish(receivedData['localId'],json.dumps(confirm),qos=1,retain=True)	
			else:
				dbIds = self.reg.consultregister(receivedData['localId'])
				if(dbIds!=False):
					#send data to IC
					self.virt.consultVirtualRes(dbIds,receivedData['data'])
					self.send.sendDataIC(dbIds,receivedData['data'])
		else:
			if(receivedData['estado']=='Virtual'):
				##### VIRTUALIZER REGISTRATION
				print('\n')
				print('VirtualSensor Register')
				if(receivedData['registred']==False):
					flag = self.virt.registerVirtualRes('sensor01','sensor02',receivedData['regInfos'])
				else:
					print('Recurso Virtual ja registrado\n')
				print('\n')
			else:
				print('Sensor without status identified')
				#if is a sensor without state
				dbIds = self.reg.registerResourceIC(receivedData['localId'],receivedData['regInfos'])
				dbIds = 'sensor01' #apenas para teste do virtualizer
				if(dbIds != False):
					#send data to IC
					print('[DEBUG]send')
					print('\n')
					self.virt.consultVirtualRes(dbIds,receivedData['data'])
					print('\n')
					self.send.sendDataIC(dbIds,receivedData['data'])
					print('\n')
		print('[MQTT]Waiting')

	def on_message(self,client,userdata,msg):
		start = timeit.timeit()
		print("Received a Message")
		receivedData = json.loads(msg.payload)
		print(receivedData)
		self.dataProcessing(client,receivedData)
		end = timeit.timeit()
		print('Runtime:')
		print(end - start)
		print('\n')		

	def startListening (self,mqttBrokerUser,mqttBrokerPassword):
		print("\033[34mSTART LISTENING MQTT INITIALIZED\033[m")
		self.mqttClient = mqtt.Client()
		self.mqttClient.username_pw_set(mqttBrokerUser,mqttBrokerPassword)
		self.mqttClient.connect(self.mqttAddress,self.mqttPort,self.mqttTimeout)
		self.mqttClient.subscribe(self.mqttTopic)	
		print('Connected')
		self.mqttClient.on_message = self.on_message	
		self.mqttClient.loop_forever()

#-----------------------------COAP--------------------------------------------
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.client.helperclient import HelperClient

class CoapClass(ProtocolClient):
	def __init__(self):
		self.port = 5683
		self.reg = Registry()
		self.send = Sender()
		#self.coapSensors = self.reg.getCoapSensors()

	def dataProcessing(self,receivedData):
		if(receivedData["registered"]!=True):
			print(receivedData['regInfos'])
			dbIds = self.reg.registerResourceIC(receivedData['localId'],receivedData['regInfos'])
			dbIds = True
			if(dbIds != False):
				print(' ')
				print('call reg')
				dbIds = self.reg.consultRegister(receivedData['localId'])
				if(dbIds!= False):
					dbIds = self.reg.registerResourceIC(receivedData['localId'],receivedData['regInfos'])
					#print(self.coapSensors)
			else:
				print('erro no cadastro')
		else:
			print('Sensor without status identified')
			#if is a sensor without state
			dbIds = self.reg.registerResourceIC(receivedData['localId'],receivedData['regInfos'])
			if(dbIds != False):
				#send data to IC
				self.send.sendDataIC(dbIds,receivedData['data'])

	def startListening(self):
		print("\033[33mSTART LISTENING COAP INITIALIZED\033[m")
		server = CoAPServer("0.0.0.0", 5683)
		try:
			server.listen(10)
		except KeyboardInterrupt:
			print ("Server Shutdown")
			server.close()
			print ("Exiting...")

	def requestSensorData(self):
			print("\033[35mREQUEST SENSOR DATA INITIALIZED\033[m")
			path = 'data'
		#for sensor in self.coapSensors:
			client = HelperClient(server=(self.coapSensors["sensor"]["address"],5683))
			self.response = client.get(path)

			self.data = json.loads(self.response.payload)
			print(self.data)

			#dbIds = self.reg.consultRegister(self.data['localId'])
			#self.send.sendDataIC(dbIds,self.data)
			print('Sended')

class BasicResource(Resource):
	def __init__(self, name="GatewayId", coap_server=None):
		super(BasicResource, self).__init__(name, coap_server, visible=True,observable=True, allow_children=True)
		self.payload = "GatewayInfos"
		self.resource_type = "rt1"
		self.content_type = "text/plain"
		self.interface_type = "if1"
		self.coapProtocolGClient = CoapClass()

	def render_POST(self, request):
		i = time.time()
		res = self.init_resource(request, BasicResource())
		print('--------------')
		print(res.payload)
		print('--------------')
		self.receivedData = json.loads(res.payload)
		self.coapProtocolGClient.dataProcessing(self.receivedData)
		f = time.time()
		print(f-i)
		return res #error 

class CoAPServer(CoAP):
	def __init__(self, host, port):
		CoAP.__init__(self, (host, port))
		self.add_resource('data/', BasicResource())


##-------------------Testbed-------------------------------##
import socket,time

class Testbed(ProtocolClient):
	def __init__(self,ip,port):
		client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		client_socket.connect((ip,port))
		time.sleep(2)

	def startListening(self):
		
		while True:
			data = client_socket.recv(512)
			if data.lower() =='q':
				client_socket.close()
				break

			print("Recebido: %s" % data)
			self.dataProcessing(self,data)

	def dataProcessing(self,receivedData):
		#check type of message, with ot without state
		if(receivedData['estado']==True):
			print('Sensor with status identified')
			if(receivedData['registered']==False):
				dbIds = self.reg.registerResourceIC(receivedData['localId'],receivedData['regInfos'])
			else:
				dbIds = self.reg.consultregister(receivedData['localId'])
				if(dbIds!=False):
					self.send.sendDataIC(dbIds,receivedData['data'])
		else:
			print('Sensor without status identified')
			#if is a sensor without state
			dbIds = self.reg.registerResourceIC(receivedData['localId'],receivedData['regInfos'])
			if(dbIds != False):
				#send data to IC
				self.send.sendDataIC(dbIds,receivedData['data'])
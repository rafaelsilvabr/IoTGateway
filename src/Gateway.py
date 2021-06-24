from protocolClients import MqttClass
from protocolClients import CoapClass
from db import DB
import threading
import time

from flask import Flask, request, jsonify, render_template
from flask.wrappers import Response

app = Flask(__name__)

@app.route('/')
def index():
    return "HW"

@app.route('/virtualizers', methods=['GET', 'POST', 'DELETE'])
def virtualizers():
    if request.method == 'GET':
        return "return all virtualizers addrs"
    if request.method == 'POST':
        try:
          data = request.get_json()
          db = DB()
          db.setVirtualizer(data["uuid"],data["addr"])
          return jsonify("{}")
        except:
            return "Erro no cadastro do virtualizador no IOTGateway"

if __name__ == "__main__":

    mqttGateway = MqttClass('gateway1','soldier.cloudmqtt.com',10514,1,'test5')
    coapGateway = CoapClass()

    mqttGateway.startListening("ctuqpqym","Xk5GNcWqcmZG")


    #sthread_coap_server = coapGateway.startListening()
    #sthread_coap_client = coapGateway.requestSensorData()


    w1 = threading.Thread(target = mqttGateway.startListening, args=("ctuqpqym","Xk5GNcWqcmZG"))
 #   w2 = threading.Thread(target = coapGateway.startListening)
#    w3 = threading.Thread(target= coapGateway.requestSensorData)
    w4 = threading.Thread(target = app.run)

    
    w1.start()
  #  w2.start()
    w4.start()

'''    while(1):
        coapGateway.requestSensorData()
        time.sleep(5)
'''
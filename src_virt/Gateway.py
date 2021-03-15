from protocolClients import MqttClass
from protocolClients import CoapClass
import threading
import time

if __name__ == "__main__":

    mqttGateway = MqttClass('gateway1','soldier.cloudmqtt.com',10514,1,'test5')
    coapGateway = CoapClass()

    #mqttGateway.startListening("ctuqpqym","Xk5GNcWqcmZG")


    #sthread_coap_server = coapGateway.startListening()
    #sthread_coap_client = coapGateway.requestSensorData()


    w1 = threading.Thread(target = mqttGateway.startListening, args=("ctuqpqym","Xk5GNcWqcmZG"))
  #  w2 = threading.Thread(target = coapGateway.startListening)
  #  w3 = threading.Thread(target= coapGateway.requestSensorData)
    
    w1.start()
  # w2.start()

'''    while(1):
        coapGateway.requestSensorData()
        time.sleep(5)
'''
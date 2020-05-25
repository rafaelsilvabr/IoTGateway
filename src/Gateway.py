from protocolClients import MqttClass
from protocolClients import CoapClass


if __name__ == "__main__":

    #gateway1 = MqttClass('gateway1','soldier.cloudmqtt.com',10514,1,'test5')
#    gateway1 = MqttClassWithoutReg('gateway1','soldier.cloudmqtt.com',10514,1,'test5')
    #gateway1.startListening("ctuqpqym","Xk5GNcWqcmZG")

    gateway2 = CoapClass()
    gateway2.startListening()
    gateway2.requestSensorData()
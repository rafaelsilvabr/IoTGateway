import json
import requests
from registry import Registry
from sender import Sender
from db import DB

class Virtualizer(object):

 def __init__(self):
  self.db = DB()
  self.reg = Registry()
  self.send = Sender()

 def registerVirtualRes(self,sensor01,sensor02,regInfos):
  print("Reg. Virtual Resource")
  flag=False
  valsensor1 = False
  valsensor2 = False

  valsensor1 = self.db.verifyDB(sensor01)
  valsensor2 = self.db.verifyDB(sensor02)

  if(valsensor1==False | valsensor2==False):
   print("IDs not in db!")
   flag = True
  else:
   print("Found in db!")

  if(flag == False):
   virt_uuid = self.reg.registerResourceIC("virt1",regInfos)
   
   if(virt_uuid != False):
    print("Virtual Sensor registered")
    flag = False
   else:
    flag = True

  return not flag

 def updateVirtualResData(self,data,idSensor):
  ##Realizar a operacao do sensor virtual, retornat todas as infos do recurso  
  #msg = {"estado":"Virtual", "registred":True, "uuid":"328913", "status": "active", "lat":10, "lon":12, "sensor1":"id1", "sensor2":"id2", "data":{"data":["temperature": 11]}}
  if(idSensor == "sensor01"):
    print("VirtualRes [Sensor01]")
    msg = {"uuid":"1234","data":{"temperatura":20}}
  if(idSensor == "sensor02"):
    print("VirtualRes [Sensor02]")
    msg = {"uuid":"1234","data":{"temperatura":45}}

  return msg


 def consultVirtualRes(self, realSensorId, data):
  print('Consult Virtual Resource initialized')
  #Buscar Virtual Sensor na DB e seus sensores
  #virtualSensor = self.db.verifyDB(realSensorId)
  virtualSensor = False
  virtualSensor = self.updateVirtualResData(data,realSensorId)
  if(virtualSensor!=False):
    self.send.sendDataIC(virtualSensor['uuid'],virtualSensor['data'])
  return virtualSensor

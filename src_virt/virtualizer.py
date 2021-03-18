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

 def registerVirtualRes(self,idsensor1,idsensor2,regInfos):
  print("Reg. Virtual Resource")
  flag=False
  valsensor1 = False
  valsensor2 = False

  valsensor1 = self.db.verifyDB(idsensor1)
  valsensor2 = self.db.verifyDB(idsensor2)

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

  def __updateVirtualResData(self,sensor1,sensor2):
    ##Realizar a operacao do sensor virtual, retornat todas as infos do recurso
    msg = {"estado":"Virtual",
        "registred":True,
        "uuid":"328913",
	      "status": "active",
	      "lat":10,
	      "lon":12,
	      "sensor1":"id1",
	      "sensor2":"id2",
      	"data":{
		      "data": [{
	          "temperature": (sensor1+sensor2)/2.0000
	        }]
	      }
    }
    return msg


 def consultVirtualRes(self, realSensorId, data):
  print('Consult Virtual Resource initialized')
  #Buscar Virtual Sensor na DB e seus sensores
  #virtualSensor = self.db.verifyDB(realSensorId)
  #  virtualSensor['data'] = self.__updateVirtualResData(data,virtualSensor['sensor2'].lastdata)
  virtualSensor = False
  if(realSensorId == 'sensor01'):
    virtualSensor ={"estado":"Virtual",
      "registred":True,
      "uuid":"328913",
      "status": "active",
      "lat":10,
      "lon":12,
      "sensor1":"id1",
      "sensor2":"id2",
      "data":{
        "data": [{
          "temperature": (30+25)/2.0
        }]
      }
    }
  if(virtualSensor!=False):
    self.send.sendDataIC(virtualSensor['uuid'],virtualSensor['data'])
  return virtualSensor

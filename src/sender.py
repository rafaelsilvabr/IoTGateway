import json
import requests
from db import DB

class Sender (object):

    def __init__(self):
        self.db = DB()

    def __prepareRegisterData(self,sensorData):
        #reading local jsons
        json_capabilities = open('capabilities.json','r')
        local_capabilities = json.load(json_capabilities)
        json_resources = open('resources.json','r')
        local_resources = json.load(json_resources)
        
        data_resource={'data':local_resources[sensorData['localId']]}
		            
        dict_capabilitie = {}
        for capabilitie in data_resource['data']['capabilities']:
            for capabilitie_data in local_capabilities[capabilitie]:
                #print(capabilitie_data)
                for loc_data in capabilitie_data:
                    #print (loc_data)
                    capabilitie_data[loc_data]=sensorData[loc_data]
            dict_capabilitie[capabilitie] = local_capabilities[capabilitie]	
        p_data = {"data":dict_capabilitie}
        print(p_data)
        return p_data

    def __requestSendDataIC(self,sensorData):
        headers= {
            'Content-type': 'application/json',
        }

        dbIds = self.db.verifyDB(sensorData['localId'])
        if(dbIds != False):            
            p_data = __prepareRegisterData(sensorData)
            try:
                response = requests.post ('http://localhost:8000/adaptor/resources/' + dbIds.uuid + '/data', data = json.dumps(p_data),headers=headers)
                print(response.text)
                if(response.text == "{}"):
                    print('Data Sent to IC')
                    print('\n')
                else:
                    print('Response Error')
            except:
                print('Request Error')

    def sendDataIC(self,sensorData):
        print("Sender Started")
        dbIds = self.db.verifyDB(sensorData['localId'])
        if(dbIds != False):
            print("Sending Data to InterSCity")
            self.__requestSendDataIC(sensorData)

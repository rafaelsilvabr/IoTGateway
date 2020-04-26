import json
import requests
from registry import Registry

class Sender (object):

    def __init__(self):
        pass

    def verifyDb(self,sensorLocalId):
        reg = Registry()
        dbIds = reg.getInDb(sensorLocalId)
        return dbIds

    def sendDataIC(self,sensorData):
        headers= {
            'Content-type': 'application/json',
        }

        json_capabilities = open('capabilities.json','r')
        local_capabilities = json.load(json_capabilities)

        json_resources = open('resources.json','r')
        local_resources = json.load(json_resources)

        data_resource={'data':local_resources[sensorData['localId']]}

        dbIds = self.verifyDb(sensorData['localId'])
        if(dbIds == False):
            print('error')
		    
        if(dbIds != False):        
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

            response = requests.post ('http://localhost:8000/adaptor/resources/' + dbIds.uuid + '/data', data = json.dumps(p_data),headers=headers)
            print('Dados Enviados IC')
            print(response.text)
            print('\n')
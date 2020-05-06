import json
import requests
from db import DB

class Sender (object):

    def __init__(self):
        self.db = DB()

    def __prepareRegisterData(self,capabilities,data):
        #reading local jsons
        json_capabilities = open('capabilities.json','r')
        local_capabilities = json.load(json_capabilities)
		            
        dict_capabilitie = {}
        for capabilitie in capabilities:
            for capabilitie_data in local_capabilities[capabilitie]:
                #print(capabilitie_data)
                for loc_data in capabilitie_data:
                    #print (loc_data)
                    try:
                        capabilitie_data[loc_data]=data[loc_data]
            dict_capabilitie[capabilitie] = local_capabilities[capabilitie]	
        p_data = {"data":dict_capabilitie}
        print(p_data)
        return p_data

    def __requestSendDataIC(self,dbIds,data):
        headers= {
            'Content-type': 'application/json',
        }

        p_data = __prepareRegisterData(dbIds.capabilities,data)
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

    def sendDataIC(self,localId,data):
        print("Sender Started")
        dbIds = self.db.verifyDB(localId)
        if(dbIds != False):
            print("Sending Data to InterSCity")
            self.__requestSendDataIC(dbIds,data)

    def sendDataIC(self,dbIds,data,bool):
        print("Sender Started")
        print("Sending Data to InterSCity")
        self.__requestSendDataIC(dbIds,data)
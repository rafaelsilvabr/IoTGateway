import json
import requests
from db import DB

class Sender (object):

    def __init__(self):
        self.db = DB()

    def __preparePostData(self,capabilities,data):
        #reading local jsons
        json_capabilities = open('capabilities.json','r')
        local_capabilities = json.load(json_capabilities)
        
        print(capabilities)
        capabilities = json.loads(capabilities)
        dict_capabilitie = {}
        for capabilitie in capabilities:
            #print(capabilitie)
            for capabilitie_data in local_capabilities[capabilitie]:
                #print(capabilitie_data)
                for loc_data in capabilitie_data:
                    #print (loc_data)
                    try:
                        capabilitie_data[loc_data]=data[loc_data]
                    except:
                        capabilitie_data[loc_data]=None
            dict_capabilitie[capabilitie] = local_capabilities[capabilitie]	
        print('Data to Pub')
        p_data = {"data":dict_capabilitie}
        print('\n')
        print(p_data)
        return p_data

    def __requestSendDataIC(self,dbIds,data):
        headers= {
            'Content-type': 'application/json',
        }

        p_data = self.__preparePostData(dbIds.capabilities,data)
        
        try:
            #response = requests.post ('http://localhost:8000/adaptor/resources/' + dbIds.uuid + '/data', data = json.dumps(p_data),headers=headers)
            response = "{}"
            #print(response.text)
            #response.text here
            if(response == "{}"):
                print('Data Sent to IC')
                print('\n')
            else:
                print('Response Error')
        except:
            print('Request Error')

    def ceSendDataIC(self,localId,data):
        print("Sender Started1")
        dbIds = self.db.verifyDB(localId)
        if(dbIds != False):
            print("Sending Data to InterSCity")
            self.__requestSendDataIC(dbIds,data)

    def seSendDataIC(self,dbIds,data):
        print("Sender Started")
        print("Sending Data to InterSCity")
        self.__requestSendDataIC(dbIds,data)
import json
import requests
from create_db import Virtualizers
from db import DB

class Sender (object):

    def __init__(self):
        self.db = DB()
        self.inctaddr = open('config.json','r')
        self.inctaddr = json.load(self.inctaddr)
        self.inctaddr = self.inctaddr['inctaddr']

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

        #p_data = self.__preparePostData(dbIds.capabilities,data)
        p_data = data
        try:
            response = requests.post (self.inctaddr + '/adaptor/resources/' + dbIds.uuid + '/data', data = json.dumps(p_data), headers=headers)
            response = "ENVIADO p/INCT"
            print(response.text)
            #response.text here
            if(response == "{}"):
                print('Data Sent to IC')
                print('\n')
                sensorVirtualizer = Virtualizers.select.where(Virtualizers.uuid == dbIds.uuid)
                for virtualizer in sensorVirtualizer:
                    requests.post ("http://" + virtualizer.uuid + "/data", data = json.dumps(p_data), headers=headers)
            else:
                print('Response Error')
        except:
            print('Request Error')


    def sendDataIC(self,dbIds,data):
        print("Sender Started")
        print("Sending Data to InterSCity")
        self.__requestSendDataIC(dbIds,data)
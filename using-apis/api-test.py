import sys
import json
import requests
"""
    api-test.py
    Eric Stadelman, 1 October 2018
    Help utilize fonoappi which provides data about mobile devices
    CS 257 Software Design class, Fall 2018.
"""

class FonApi:

    __api_url = 'https://fonoapi.freshpixl.com/v1/'


    #initializes api_key and self.api_url
    def __init__(self, api_key):
        api_key = "e3dc5bb3533fd53f9cd9bd2149b86a957a884532125e9a8e"
        self.__api_url = FonApi.__api_url
        self.__api_key = api_key


    #calls sendpostdata and saves all the info to result
    def get_info(self, brand, action):
        url = self.__api_url + 'getdevice'
        postdata = {'device': brand, 'token': self.__api_key}
        headers = {'content-type': 'application/json'}
        result = self.sendpostdata(url, postdata, headers)
        
        #saves all device names to phone_list
        if action == "company":
            phone_list=[]
            try:
                for phone in result.json():
                    phone_list.append(phone['DeviceName'])
                return(phone_list)
            except AttributeError:
                return result

        #returns all info about a device
        if action == "device":
            try:
                return result.json()
            except AttributeError:
                return result            


    def sendpostdata(self, url, postdata, headers, result = None):
        try:
            result = requests.post(url, data=json.dumps(postdata), headers=headers)
            return result

        #if not connected to the internet throws an error
        except requests.exceptions.RequestException as e:
            return "Connect error. Check URL"


def main():
    myvariable = FonApi("")

    if len(sys.argv) == 1:
        print("please enter either 'company' followed by a company name or 'device' followed by a device name.")

    elif sys.argv[1].lower() == "company":
        print(myvariable.get_info(sys.argv[2] , "company"))

    #creates a string of all command line arguments after the first 2 for the device name 
    elif sys.argv[1].lower() == "device":
        device_name = ""
        for x in sys.argv:
            if x != sys.argv[0]:
                if x != sys.argv[1]:
                    device_name += " "
                    device_name += x 
        print(myvariable.get_info(device_name, "device"))

    elif sys.argv[1].lower() != "company" and sys.argv[1].lower() != "device":
            print("please enter either 'company' followed by a company name or 'device' followed by a device name.")
main()







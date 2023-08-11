from .serverStatus import returnstatus
import requests
import time
from .json_Save import *


def startMonitorMode():
    try:
        monitorConfig = getJSON("./functions/data/monitorconfig.json")
        while(True):
            sta = returnstatus()
            print("[#]STATUS ENVIADO")
            response =  requests.get(f"{monitorConfig['serverprotocol']}://{monitorConfig['serveradress']}/api/statusservice/sendstatus")
            sta['csrfmiddlewaretoken'] = response.json()["csrf_token"]
            sta['token'] = monitorConfig['token']
            response =  requests.post(f"{monitorConfig['serverprotocol']}://{monitorConfig['serveradress']}/api/statusservice/sendstatus",data=sta,cookies=response.cookies)
            print(response.json())
            time.sleep(1)
    except Exception as e:
        return f"<ERROR: {str(e)}>"

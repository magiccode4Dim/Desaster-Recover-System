from .serverStatus import returnstatus
import requests
import time
from .json_Save import *


def startMonitorMode():
    old_download = 0
    old_upload=0
    try:
        monitorConfig = getJSON("./functions/data/monitorconfig.json")
        while True:
            sta = returnstatus()
            upload_speed = sta["totalup"]
            download_speed = sta["totaldown"]
            upload_now = upload_speed - old_upload
            download_now = download_speed - old_download
            sta["nowup"] = round(upload_now,2) 
            sta["nowdown"] = round(download_now,2)
            print(sta) 
            old_upload = upload_speed
            old_download = download_speed
            response =  requests.get(f"{monitorConfig['serverprotocol']}://{monitorConfig['serveradress']}/api/statusservice/sendstatus")
            sta['csrfmiddlewaretoken'] = response.json()["csrf_token"]
            sta['token'] = monitorConfig['token']
            response =  requests.post(f"{monitorConfig['serverprotocol']}://{monitorConfig['serveradress']}/api/statusservice/sendstatus",data=sta,cookies=response.cookies)
            print(response.json())
            time.sleep(1)
    except Exception as e:
        return f"<ERROR: {str(e)}>"



from serverStatus import returnstatus
import requests
import time

if __name__=="__main__":
    while(True):
        sta = returnstatus()
        print(sta)
        #get csrf_token
        response =  requests.get("http://127.0.0.1:8000/api/statusservice/sendstatus")
        sta['csrfmiddlewaretoken'] = response.json()["csrf_token"]
        sta['token'] = 'KC8us4mWDtAMcKWHd8L7b2Comx-pzLwN6b2TCfE4xeU8275012e3d644533b233eb90ed957ad1'
        response =  requests.post("http://127.0.0.1:8000/api/statusservice/sendstatus",data=sta,cookies=response.cookies)
        print(response.json())
        time.sleep(1)

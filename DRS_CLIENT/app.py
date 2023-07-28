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
        sta['token'] = 'RiSz5mCTcFeC1dcoFTOA1VV0y67Fg8mu-NLhlgRZD4gb5f53d08fd2e4897865ee5ea7129c955'
        response =  requests.post("http://127.0.0.1:8000/api/statusservice/sendstatus",data=sta,cookies=response.cookies)
        print(response.json())
        time.sleep(1)

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
        sta['token'] = 'BJSt6XOH34F3c8mtoPcgdtdrrPoMrLNEreA1aKQ3GoQ75df5d367248467db3009ea9816772fc'
        response =  requests.post("http://127.0.0.1:8000/api/statusservice/sendstatus",data=sta,cookies=response.cookies)
        print(response.json())
        time.sleep(3)
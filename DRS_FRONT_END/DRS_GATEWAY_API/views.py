from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,JsonResponse
import json
from django.middleware.csrf import get_token
from DRS_WEB_APP.modulos.requests.eurekaservermethods import *
from DRS_WEB_APP.modulos.requests.sendRequests import *
from django.contrib.auth.decorators import login_required

WEB_PATH = '/web'

STATUS_SERVICE = {
    "name" : 'STATUS_SERVICE',
    "username" : "nany",
    "password" :"2001",
    "protocol" : "http"
}

#get last status
def getStatusByID(id):
        serverStatus = get_microservice_address_port(STATUS_SERVICE["name"])
        if(serverStatus['port']!=0):
            status = get_microservice_data(STATUS_SERVICE["username"],STATUS_SERVICE["password"],
                                  serverStatus['address'],serverStatus['port'],STATUS_SERVICE["protocol"],
                                  path='drs/api/status/getlaststatus/'+id)
        else:
             status = None
        return  status


#getlaststatus of server
@login_required
def getlaststatusServer(request):
    serverID =  request.GET.get("id")
    return JsonResponse(getStatusByID(serverID))
    
    

#send status to server
class StatusService(View):
    def get(self, request):
        csrf_token = get_token(request)
        return JsonResponse({'csrf_token': csrf_token})

    def post(self, request):
        cpu = request.POST.get("cpu")
        memory = request.POST.get("memory")
        disc = request.POST.get("disc")
        token  = request.POST.get("token")
        #print(request.body)
        #print(f"cpu = {cpu} memory = {memory} disc = {disc}")
        try:
            totalup = request.POST.get("totalup")
            totaldown = request.POST.get("totaldown")
            nowup = request.POST.get("nowup")
            nowdown = request.POST.get("nowdown")
        except Exception as e:
            totalup = 0
            totaldown = 0
            nowup = 0
            nowdown = 0
        status = {
            "value": True,
            "token":token,
            "cpu":float(cpu),
            "memory":float(memory),
            "disc":float(disc),
            "totalup" : float(totalup),
            "totaldown" : float(totaldown),
            "nowup" : float(nowup),
            "nowdown" : float(nowdown)
        }
        #print(status)
        serverImage = get_microservice_address_port(STATUS_SERVICE["name"])
        url = STATUS_SERVICE["protocol"]+"://"+serverImage['address']+":"+str(serverImage['port'])+"/drs/api/status/create"
        respo = sendPostRequest(json = status,adress=url
                                ,username=STATUS_SERVICE["username"], password=STATUS_SERVICE["password"])
        
        return JsonResponse(respo)
    
    def put(self, request):
        return HttpResponse("This is a PUT request.")

    def delete(self, request):
        return HttpResponse("This is a DELETE request.")
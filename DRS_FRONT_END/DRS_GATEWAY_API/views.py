from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,JsonResponse
import json
from django.middleware.csrf import get_token
from DRS_WEB_APP.modulos.requests.eurekaservermethods import *
from DRS_WEB_APP.modulos.requests.sendRequests import *

WEB_PATH = '/web'

STATUS_SERVICE = {
    "name" : 'STATUS_SERVICE',
    "username" : "nany",
    "password" :"2001",
    "protocol" : "http"
}

class StatusService(View):
    def get(self, request):
        csrf_token = get_token(request)
        return JsonResponse({'csrf_token': csrf_token})

    def post(self, request):
        cpu = request.POST.get("cpu")
        memory = request.POST.get("memory")
        disc = request.POST.get("disc")
        token  = request.POST.get("token")
        print(f"cpu = {cpu} memory = {memory} disc = {disc}")
        status = {
            "value": True,
            "token":token,
            "cpu":float(cpu),
            "memory":float(memory),
            "disc":float(disc)
        }
        serverImage = get_microservice_address_port(STATUS_SERVICE["name"])
        url = STATUS_SERVICE["protocol"]+"://"+serverImage['address']+":"+str(serverImage['port'])+"/drs/api/status/create"
        respo = sendPostRequest(json = status,adress=url
                                ,username=STATUS_SERVICE["username"], password=STATUS_SERVICE["password"])
        
        return JsonResponse(respo)
    
    def put(self, request):
        return HttpResponse("This is a PUT request.")

    def delete(self, request):
        return HttpResponse("This is a DELETE request.")
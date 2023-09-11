from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,JsonResponse,FileResponse
import json
from django.middleware.csrf import get_token
from DRS_WEB_APP.modulos.requests.eurekaservermethods import *
from DRS_WEB_APP.modulos.requests.sendRequests import *
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
import os
from django.conf import settings

WEB_PATH = '/web'
API_GATEWAY ="/DRS_GATEWAY_API"

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
        
        totalup = request.POST.get("totalup")
        totaldown = request.POST.get("totaldown")
        nowup = request.POST.get("nowup")
        nowdown = request.POST.get("nowdown")

        #computer info
        fcores = request.POST.get("fcores")
        vcores = request.POST.get("vcores")
        freq = request.POST.get("freq")
        men = request.POST.get("men")

        print(token)

        if(totalup==None):
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
            "nowdown" : float(nowdown),
            "fcores":fcores,
            "vcores":vcores,
            "freq":float(freq),
            "men":float(men)
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

#Baixar a ficheiros da pasta download
def downloadFiles(request):
    file =  request.GET.get("file")
    relative_path = f'downloads/{file}'
    file_path = static(relative_path)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+API_GATEWAY
    #file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', relative_path))
    #print(BASE_DIR+file_path)
    if os.path.exists(BASE_DIR+file_path):
                file = open(BASE_DIR+file_path, 'rb')
                response = FileResponse(file)
                response['Content-Type'] = 'application/zip'
                # Defina o cabeçalho de resposta para anexar o arquivo
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                #file.close()
                return response
    else:
        return HttpResponse("Arquivo não encontrado", status=404)
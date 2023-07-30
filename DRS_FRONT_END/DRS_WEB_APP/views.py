from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User

from django.views import View
from django.utils.decorators import method_decorator
from .modulos.requests.eurekaservermethods import get_microservice_address_port,get_microservice_data
from .modulos.requests.sendRequests import *
import json

WEB_PATH = '/web'

IMAGE_SERVICE = {
    "name" : 'IMAGE_SERVICE',
    "username" : "nany",
    "password" :"2001",
    "protocol" : "http"
}
STATUS_SERVICE = {
    "name" : 'STATUS_SERVICE',
    "username" : "nany",
    "password" :"2001",
    "protocol" : "http"
}
BACKUP_SERVICE = {
    "name" : 'BACKUP_SERVICE',
    "username" : "nany",
    "password" :"2001",
    "protocol" : "http"
}

#Login
#redirect to login
def redirect_login(request):
    return redirect('/web/login')

@login_required
def dashBoard(request):
    return render(request,'userpages/dashboard.html',{'user':request.user})

#manage volumes
#manageVolumes
@method_decorator(login_required, name='dispatch')
class  manageVolumes(View):
    def getVolumes(self):
        serverBackup = get_microservice_address_port(BACKUP_SERVICE["name"])
        if(serverBackup['port']!=0):
            volumes = get_microservice_data(BACKUP_SERVICE["username"],BACKUP_SERVICE["password"],
                                  serverBackup['address'],serverBackup['port'],BACKUP_SERVICE["protocol"],
                                  path='drs/api/backup/volumes/getall')
        else:
             volumes = []
        return  volumes
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        done = request.GET.get('done')
        volumes = self.getVolumes()
        #print(volumes)
        return render(request,"userpages/manageVolumes.html",{"error":error_message, 
                                                              "done":done,
                                                              "volumes":volumes["Volumes"]
                                                              })
    def post(self, request, *args, **kwargs):
        return self.get(request)
    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)


#new volume
#newVolume
@method_decorator(login_required, name='dispatch')
class  newVolume(View):
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        return render(request,'userpages/criateVolume.html',{"error":error_message})
    def post(self, request, *args, **kwargs):
        nome = request.POST.get("nome")
        label = request.POST.get("label")
        if(len(nome)==0 or len("label")==0):
            return redirect(WEB_PATH+"/volumes/create?error=Algum Campo não foi preenchido")
        newvolume = {
            "nome":nome,
            "label":label
        }
        serverbackup = get_microservice_address_port(BACKUP_SERVICE["name"])
        url = BACKUP_SERVICE["protocol"]+"://"+serverbackup['address']+":"+str(serverbackup['port'])+"/drs/api/backup/volumes/create"
        respo = sendPostRequest(json = newvolume,adress=url
                                ,username=BACKUP_SERVICE["username"], password=BACKUP_SERVICE["password"])
        try:
            created  = respo["CreatedAt"]
            return redirect(WEB_PATH+f"/volumes/manager?done=Volume {nome} Adicionado com Sucesso")
        except Exception as e:
            return redirect(WEB_PATH+"/volumes/create?error=Erro "+str(respo))

    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)


#server detains
#serverDetails
@method_decorator(login_required, name='dispatch')
class  serverDetails(View):
    def getServerByID(self,id):
        serverStatus = get_microservice_address_port(STATUS_SERVICE["name"])
        if(serverStatus['port']!=0):
            server = get_microservice_data(STATUS_SERVICE["username"],STATUS_SERVICE["password"],
                                  serverStatus['address'],serverStatus['port'],STATUS_SERVICE["protocol"],
                                  path='drs/api/status/server/get/'+id)
        else:
             server = None
        return  server
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        serverID = request.GET.get('id')
        server  = self.getServerByID(serverID)
        response =render(request,'userpages/serverDetails.html',{"error":error_message, 
                                                                 "server": server})
        response.set_cookie('serverID', serverID)
        response.set_cookie('apiurl', request.META.get('HTTP_HOST', None))
        response.set_cookie('protocol', request.scheme)
        
        return response        
    def post(self, request, *args, **kwargs):
        return self.get(request)
    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)


#manage servers
#manageServers
@method_decorator(login_required, name='dispatch')
class  manageServers(View):
    def getServers(self):
        serverStatus = get_microservice_address_port(STATUS_SERVICE["name"])
        if(serverStatus['port']!=0):
            servers = get_microservice_data(STATUS_SERVICE["username"],STATUS_SERVICE["password"],
                                  serverStatus['address'],serverStatus['port'],STATUS_SERVICE["protocol"],
                                  path='drs/api/status/server/getall')
        else:
             servers = []
        return  servers
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        done = request.GET.get('done')
        servers = self.getServers()
        return render(request,"userpages/manageServers.html",{"error":error_message, 
                                                              "done":done,
                                                              "servers":servers
                                                              })
    def post(self, request, *args, **kwargs):
        return self.get(request)
    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)

#createServer
@method_decorator(login_required, name='dispatch')
class  createServer(View):
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        return render(request,"userpages/criateServer.html",{"error":error_message})
    def post(self, request, *args, **kwargs):
        serverAdress =  request.POST.get("serverAdress")
        nome = request.POST.get("nome")
        if(len(serverAdress)==0 or len(nome)==0):
            return redirect(WEB_PATH+"/server/create?error=Algum Campo não foi preenchido")
        newServer = {
               'serverAdress': serverAdress,
               'nome': nome
        }
        serverImage = get_microservice_address_port(STATUS_SERVICE["name"])
        url = STATUS_SERVICE["protocol"]+"://"+serverImage['address']+":"+str(serverImage['port'])+"/drs/api/status/server/create"
        respo = sendPostRequest(json = newServer,adress=url
                                ,username=STATUS_SERVICE["username"], password=STATUS_SERVICE["password"])
        if(respo["response"]==200):
            return redirect(WEB_PATH+"/server/manager?done=Servidor Adicionado com Sucesso")
        return self.get(request)
    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)
#push container
@method_decorator(login_required, name='dispatch')
class  pushImage(View):
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        repo = request.GET.get('repo')
        return render(request,"userpages/pushtoregistry.html",{"error":error_message, 
                                                                 "repo": repo})
    def post(self, request, *args, **kwargs):
        repo = request.POST.get("repo")
        image = {
            "nome":repo
        }
        serverImage = get_microservice_address_port(IMAGE_SERVICE["name"])
        url = IMAGE_SERVICE["protocol"]+"://"+serverImage['address']+":"+str(serverImage['port'])+"/drs/api/image/pushtoregistry"
        respo = sendPostRequest(json = image,adress=url
                                ,username=IMAGE_SERVICE["username"], password=IMAGE_SERVICE["password"])
        #deve retornar para o registry
        return self.get(request)
    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)
#Save container as image
@method_decorator(login_required, name='dispatch')
class  saveContainerasImage(View):
    def getRegistrys(self):
        serverImage = get_microservice_address_port(IMAGE_SERVICE["name"])
        if(serverImage['port']!=0):
            registryList = get_microservice_data(IMAGE_SERVICE["username"],IMAGE_SERVICE["password"],
                                  serverImage['address'],serverImage['port'],IMAGE_SERVICE["protocol"],
                                  path='drs/api/image/registry/getall')
        else:
             registryList = []
        return registryList
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        registryList = self.getRegistrys()
        return render(request,'userpages/saveasimage.html',{
            "error":error_message,
            "containerID" : request.GET.get('id'),
            "registrys":registryList
        })
    def post(self, request, *args, **kwargs):
        imagename =  request.POST.get("imagename")
        tag =  request.POST.get("tag")
        registryip =  request.POST.get("ipregistry")
        containerid = request.POST.get("containerid")
        if(len(imagename)==0 or len(tag)==0  or registryip not in self.getRegistrys()):
            return redirect(WEB_PATH+"/container/saveasimage?error=Algum Campo não foi preenchido&id="+str(containerid))
        #minusculas
        imagename = imagename.lower()
        tag = tag.lower()
        #mudando o nome do container
        newImage = {
            "nome":registryip+"/"+imagename,
            "tag":tag,
            "containerID":containerid
            }
        serverImage = get_microservice_address_port(IMAGE_SERVICE["name"])
        url = IMAGE_SERVICE["protocol"]+"://"+serverImage['address']+":"+str(serverImage['port'])+"/drs/api/image/container/saveasimage"
        respo = sendPostRequest(json = newImage,adress=url
                                ,username=IMAGE_SERVICE["username"], password=IMAGE_SERVICE["password"])
        if(respo["response"]==201):
            #container/push
              return render(request,"userpages/pushtoregistry.html",{"repo": registryip+"/"+imagename})
        return redirect(WEB_PATH+f"/container/saveasimage?error=Algum Erro Aconteceu {str(respo)}&id="+str(containerid))
    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)


#Container Details
@method_decorator(login_required, name='dispatch')
class  containerDetails(View):
    def getContainerByID(self,id):
        serverImage = get_microservice_address_port(IMAGE_SERVICE["name"])
        if(serverImage['port']!=0):
            containers = get_microservice_data(IMAGE_SERVICE["username"],IMAGE_SERVICE["password"],
                                  serverImage['address'],serverImage['port'],IMAGE_SERVICE["protocol"],
                                  path='drs/api/image/container/get/'+id)
        else:
             containers = None
        return  containers
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        container =  self.getContainerByID(request.GET.get('id'))
        containerText = str(container)
        containerText = containerText.replace(",",",\n")
        return render(request,'userpages/containerDetails.html',{"error":error_message, 
                                                                 "container": container,
                                                                 "containertxt":containerText})
    def post(self, request, *args, **kwargs):
        return self.get(request)
    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)

#manage replicas
@method_decorator(login_required, name='dispatch')
class  manageContainers(View):
    def getAvailableContainers(self):
        serverImage = get_microservice_address_port(IMAGE_SERVICE["name"])
        if(serverImage['port']!=0):
            containers = get_microservice_data(IMAGE_SERVICE["username"],IMAGE_SERVICE["password"],
                                  serverImage['address'],serverImage['port'],IMAGE_SERVICE["protocol"],
                                  path='drs/api/image/container/getall')
        else:
             containers = []
        return  containers
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        containers =  self.getAvailableContainers()
        return render(request,'userpages/manageContainers.html',{"error":error_message, "containers": containers})
    def post(self, request, *args, **kwargs):
        return ""
    def put(self, request, *args, **kwargs):
        return ""
    def delete(self, request, *args, **kwargs):
        return ""


#create Container
@method_decorator(login_required, name='dispatch')
class  newContainer(View):
    def getImage(self,imageName):
        images  = self.getAvailableImages()
        for i in images:
            if (i["nome"] == imageName):
                return i
        return None
    
    def getAvailableImages(self):
        serverImage = get_microservice_address_port(IMAGE_SERVICE["name"])
        if(serverImage['port']!=0):
            imagesAvailable = get_microservice_data(IMAGE_SERVICE["username"],IMAGE_SERVICE["password"],
                                  serverImage['address'],serverImage['port'],IMAGE_SERVICE["protocol"],
                                  path='drs/api/image/getall')
        else:
             imagesAvailable = []
        return  imagesAvailable
    
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        #pegar as imagens disponiveis
        self.imagesAvailable = self.getAvailableImages()
        return render(request,'userpages/createContainer.html',{"error":error_message, "imageslist": self.imagesAvailable})
    def post(self, request, *args, **kwargs):
        name = request.POST['name_cc']
        username = request.POST['username_cc']
        password = request.POST['password_cc']
        hostname = request.POST['hostname_cc']
        image = request.POST['image_cc']
        print(password)
        try:
            im = self.getImage(image)
            if image == None:
                #imagem nao disponivel
                return redirect(WEB_PATH+"/container/create?error=Imagem não Disponivel")
            if(len(name)>0 and len(username)>0 and len(password)>0 and len(hostname)>0):
                #cria o contaimer
                container = {
                    "name":name,
                    "image":image,
                    "hostname":hostname,
                    "username":username,
                    "password":password
                }
                serverImage = get_microservice_address_port(IMAGE_SERVICE["name"])
                url = IMAGE_SERVICE["protocol"]+"://"+serverImage['address']+":"+str(serverImage['port'])+"/drs/api/image/container/create"
                respo = sendPostRequest(json = container,adress=url
                                ,username=IMAGE_SERVICE["username"], password=IMAGE_SERVICE["password"])
                try:
                    a = respo['ssh_p']
                    return render(request,'userpages/createContainer_done.html',{"jsondata":respo, "usernamessh":username,"passwordssh":password}) 
                except Exception as e:
                    return render(request,'userpages/createContainer_done.html',{"jsondataerror":respo})
                #return JsonResponse(respo)
            else:
                return redirect(WEB_PATH+"/container/create?error=Algum Campo não foi preenchido")
                #cria nova imagem
        except Exception as e:
            print(e)
            return redirect(WEB_PATH+"/container/create?error=Algum Erro Aconteceu")
        self.get(request)
    def put(self, request, *args, **kwargs):
        return render(request,'userpages/createContainer.html',{"error":"error_message"})

    def delete(self, request, *args, **kwargs):
        return render(request,'userpages/createContainer.html',{"error":"error_message"})  
    


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

from DRS_GATEWAY_API.views import getStatusByID

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
MANAGER_SERVICE = {
    "name" : 'MANAGER_SERVICE',
    "username" : "nany",
    "password" :"2001",
    "protocol" : "http"
}
FAILOVER_SERVICE = {
    "name" : 'FAILOVER_SERVICE',
    "username" : "nany",
    "password" :"2001",
    "protocol" : "http"
}

#Esses sao nos do cluster cujo servidores devem ter os mesmos nomes se quisermos fazer monitoramento
CLUSTER_NODES=["MASTER","WORKER1","WORKER2","REGISTRY"]


def getNodesInfo():
    nodesinfos = list()
    for n in CLUSTER_NODES:
        lastis = getStatusByID(n)
        lastis["node"]=n
        nodesinfos.append(lastis)
    return nodesinfos



#Login
#redirect to login
def redirect_login(request):
    return redirect('/web/login')

#GLOBAL METODOS START
#get volumes
def getVolumes():
        serverBackup = get_microservice_address_port(BACKUP_SERVICE["name"])
        if(serverBackup['port']!=0):
            volumes = get_microservice_data(BACKUP_SERVICE["username"],BACKUP_SERVICE["password"],
                                  serverBackup['address'],serverBackup['port'],BACKUP_SERVICE["protocol"],
                                  path='drs/api/backup/volumes/getall')
        else:
             volumes = []
        return  volumes
#get available images
def getAvailableImages():
        serverImage = get_microservice_address_port(IMAGE_SERVICE["name"])
        if(serverImage['port']!=0):
            imagesAvailable = get_microservice_data(IMAGE_SERVICE["username"],IMAGE_SERVICE["password"],
                                  serverImage['address'],serverImage['port'],IMAGE_SERVICE["protocol"],
                                  path='drs/api/image/getall')
        else:
             imagesAvailable = []
        return  imagesAvailable
#get image by name
def getImage(imageName):
        images  = getAvailableImages()
        for i in images:
            if (i["nome"] == imageName):
                return i
        return None

#networks
def getNets():
        server = get_microservice_address_port(MANAGER_SERVICE["name"])
        if(server['port']!=0):
            nets = get_microservice_data(MANAGER_SERVICE["username"],MANAGER_SERVICE["password"],
                                  server['address'],server['port'],MANAGER_SERVICE["protocol"],
                                  path='drs/api/manager/networks/getall')
        else:
             nets = []
        return nets
#get services
def getServices():
        server = get_microservice_address_port(MANAGER_SERVICE["name"])
        if(server['port']!=0):
            services = get_microservice_data(MANAGER_SERVICE["username"],MANAGER_SERVICE["password"],
                                  server['address'],server['port'],MANAGER_SERVICE["protocol"],
                                  path='drs/api/manager/services/getall')
        else:
             services = []
        return services
#get services from db
def getServicesDB():
        server = get_microservice_address_port(MANAGER_SERVICE["name"])
        if(server['port']!=0):
            services = get_microservice_data(MANAGER_SERVICE["username"],MANAGER_SERVICE["password"],
                                  server['address'],server['port'],MANAGER_SERVICE["protocol"],
                                  path='drs/api/manager/services/getalldb')
        else:
             services = []
        return services
#get all failovers
def getFailovers():
        server = get_microservice_address_port(FAILOVER_SERVICE["name"])
        if(server['port']!=0):
            failsovers = get_microservice_data(FAILOVER_SERVICE["username"],FAILOVER_SERVICE["password"],
                                  server['address'],server['port'],FAILOVER_SERVICE["protocol"],
                                  path='drs/api/failover/getall')
        else:
             failsovers = []
        return failsovers
#verifica se um determinado nome de servico existe
def serviceNameExists(sname):
        server = get_microservice_address_port(FAILOVER_SERVICE["name"])
        res = get_microservice_data(FAILOVER_SERVICE["username"],FAILOVER_SERVICE["password"],
                                  server['address'],server['port'],FAILOVER_SERVICE["protocol"],
                                  path='drs/api/failover/exists/'+str(sname))
 
        return res["res"]

#GLOBAL METODOS END

def convertArraytostring(array):
    comma_separated_string = ','.join(array)
    return comma_separated_string 


@login_required
def dashBoard(request):
        response =render(request,'userpages/dashboard.html',
            {'user':request.user,'adress':request.scheme+"://"+request.META.get('HTTP_HOST', None), 
            'file':"AAEE_WARS_NODE.zip", 'file2':"AAEE_WARS_SERVER.zip",'clusterservers':getNodesInfo()})
        response.set_cookie("nodes",convertArraytostring(CLUSTER_NODES))
        response.set_cookie('apiurl', request.META.get('HTTP_HOST', None))
        response.set_cookie('protocol', request.scheme)
        return response  

#detele image
@login_required
def deleteImage(request):
    id = request.GET.get("id")
    nome = request.GET.get("nome")
    server = get_microservice_address_port(IMAGE_SERVICE["name"])
    baseurl = IMAGE_SERVICE["protocol"]+"://"+server['address']+":"+str(server['port'])+"/drs/api/image/"
    url = baseurl+"deleteoncluster/"+str(nome)
    respo = sendDeleteRequest(json = None,adress=url,username=IMAGE_SERVICE["username"], password=IMAGE_SERVICE["password"])
    if(respo["response"]==200):
        url = baseurl+"delete/"+str(id)
        respo = sendDeleteRequest(json = None,adress=url,username=IMAGE_SERVICE["username"], password=IMAGE_SERVICE["password"])
        return redirect(WEB_PATH+f"/images/manager?done= Imagem Apagada com sucesso")
    else:
         return redirect(WEB_PATH+f"/images/manager?error= Erro {str(respo)}")

#create Container JSON
@method_decorator(login_required, name='dispatch')
class  newContainerJson(View):
    
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        #pegar as imagens disponiveis
        #self.imagesAvailable = getAvailableImages()
        return render(request,'userpages/createContainerJson.html',{"error":error_message})
    def post(self, request, *args, **kwargs):
        newContainer = request.POST['containerjson']
        name = request.POST['name']
        try:
            if(len(newContainer)>0 and len(name)>0 ):
                #cria o contaimer
                try:
                    s = json.loads(newContainer)
                except Exception as e:
                    return redirect(WEB_PATH+"/containerjson/create?error=Existe Algum erro no objecto Json")
                serverImage = get_microservice_address_port(IMAGE_SERVICE["name"])
                url = IMAGE_SERVICE["protocol"]+"://"+serverImage['address']+":"+str(serverImage['port'])+"/drs/api/image/containerjson/create/"+str(name)
                respo = sendPostRequest(json = s,adress=url
                                ,username=IMAGE_SERVICE["username"], password=IMAGE_SERVICE["password"])
                if(respo["response"]==204):
                    return redirect(WEB_PATH+f"/container/manager?done= Container Criado com sucesso")
                else:
                    return redirect(WEB_PATH+f"/container/manager?error="+str(respo))
                #return JsonResponse(respo)
            else:
                return redirect(WEB_PATH+"/containerjson/create?error=Introduza o Objecto Json")
                #cria nova imagem
        except Exception as e:
            print(e)
            return redirect(WEB_PATH+"/container/create?error=Algum Erro Aconteceu")
        self.get(request)
    def put(self, request, *args, **kwargs):
        return render(request,'userpages/createContainer.html',{"error":"error_message"})

    def delete(self, request, *args, **kwargs):
        return render(request,'userpages/createContainer.html',{"error":"error_message"})  
    




#manage images
@method_decorator(login_required, name='dispatch')
class  manageImages(View):
    
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        done = request.GET.get('done')
        volumes = getVolumes()
        #print(volumes)
        try:
            images = getAvailableImages()
        except Exception as e:
            pass
        return render(request,"userpages/manageImages.html",{"error":error_message, 
                                                              "done":done,
                                                              "images":images
                                                    })
    def post(self, request, *args, **kwargs):
        return self.get(request)
    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)


#delete failover
@login_required
def deleteFailover(request):
    id = request.GET.get("id")
    server = get_microservice_address_port(FAILOVER_SERVICE["name"])
    url = FAILOVER_SERVICE["protocol"]+"://"+server['address']+":"+str(server['port'])+"/drs/api/failover/delete/"+str(id)
    respo = sendDeleteRequest(json = None,adress=url,username=FAILOVER_SERVICE["username"], password=FAILOVER_SERVICE["password"])
    if(respo["response"]==200):
        return redirect(WEB_PATH+f"/failover/manager?done= Failover Apagado Com sucesso")
    else:
         return redirect(WEB_PATH+f"/failover/create?error= Erro {str(respo)}")

#Criate image with dockerfile
@method_decorator(login_required, name='dispatch')
class  newImage(View):
    def createImage(self, im):
        serverImage = get_microservice_address_port(IMAGE_SERVICE["name"])
        url = IMAGE_SERVICE["protocol"]+"://"+serverImage['address']+":"+str(serverImage['port'])+"/drs/api/image/build"
        respo = sendPostRequest(json = im,adress=url
                                ,username=IMAGE_SERVICE["username"], password=IMAGE_SERVICE["password"])
        return respo
    def createnewImage(self, im):
        serverImage = get_microservice_address_port(IMAGE_SERVICE["name"])
        url = IMAGE_SERVICE["protocol"]+"://"+serverImage['address']+":"+str(serverImage['port'])+"/drs/api/image/createnewimage"
        respo = sendPostRequest(json = im,adress=url
                                ,username=IMAGE_SERVICE["username"], password=IMAGE_SERVICE["password"])
        return respo

    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        return render(request,"userpages/criateImage.html",{"error":error_message, 
                                                    })
    def post(self, request, *args, **kwargs):
        nome =  request.POST.get("nome")
        tag =  request.POST.get("tag")
        dockerfile = request.POST.get("dockerfile")
        if(len(nome)==0 or len(tag)==0 or len(dockerfile)==0):
            return redirect(WEB_PATH+"/image/create?error=Algum Campo não foi preenchido")
        
        image =  {
            "remote":dockerfile,
            "t":str(nome)+":"+str(tag)
            }
        
        res= self.createImage(image)
        
        if(res["response"]==200):
            self.createnewImage({
                "nome":nome,
                "tag":tag
                })
            return redirect(WEB_PATH+f"/images/manager?done= Imagem {nome} criada com Sucesso")
        else:
            return redirect(WEB_PATH+f"/images/create?error= Erro {str(res)}")
        return self.get(request)
    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)



#failover list
#manage services
@method_decorator(login_required, name='dispatch')
class  manageFailovers(View):
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        done = request.GET.get('done')
        fo =  getFailovers()
        return render(request,"userpages/manageFailovers.html",{"error":error_message, 
                                                              "done":done,
                                                              "failovers":fo
                                                    })
    def post(self, request, *args, **kwargs):
        return self.get(request)
    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)


#create new failover
@method_decorator(login_required, name='dispatch')
class  newFailover(View):
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        services = getServicesDB()
        return render(request,'userpages/createFailover.html',{"error":error_message, "services":services})
    def post(self, request, *args, **kwargs):
        nome = request.POST.get("nome")
        serverid = request.POST.get("serverid")
        if(len(nome)==0 or len(serverid)==0):
            return redirect(WEB_PATH+"/failover/create?error=Algum Campo não foi preenchido")
        servicesToCreate = list()
        #verificar se a pessoa marcou um servicos
        services = getServicesDB()
        for s in services:
            if(request.POST.get(s["id"])!=None):
                servicesToCreate.append(s["service"])     
        if(len(servicesToCreate)==0):
            return redirect(WEB_PATH+"/failover/create?error=Deve selecionar Pelomenos 1 Servico")
        failover = {
            "nome":nome,
            "serverID":serverid,
            "services":servicesToCreate
        }
        server = get_microservice_address_port(FAILOVER_SERVICE["name"])
        url = FAILOVER_SERVICE["protocol"]+"://"+server['address']+":"+str(server['port'])+"/drs/api/failover/create"
        respo = sendPostRequest(json = failover,adress=url
                                ,username=FAILOVER_SERVICE["username"], password=FAILOVER_SERVICE["password"])
        if(respo["response"]==200):
            #depois de criar o fail over, o servico em execucao deve ser apagado 
            #para que e, ele sera iniciado somente quando o failover acontecer
            for sd in servicesToCreate:
                server = get_microservice_address_port(MANAGER_SERVICE["name"])
                url = MANAGER_SERVICE["protocol"]+"://"+server['address']+":"+str(server['port'])+"/drs/api/manager/services/delete/"+str(sd["Name"])
                respo = sendDeleteRequest(json = None,adress=url,username=MANAGER_SERVICE["username"], password=MANAGER_SERVICE["password"])
            return redirect(WEB_PATH+"/failover/manager?done=Failover criado com sucesso")
        elif(respo["response"]==500):
            return redirect(WEB_PATH+"/failover/create?error=Ocorreu algum erro")
        else:
            return redirect(WEB_PATH+f"/failover/create?error={str(respo)}")


    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)

#Service details
@method_decorator(login_required, name='dispatch')
class  serviceDetails(View):
    def getServiceByID(self,id):
        server = get_microservice_address_port(MANAGER_SERVICE["name"])
        if(server['port']!=0):
            service = get_microservice_data(MANAGER_SERVICE["username"],MANAGER_SERVICE["password"],
                                  server['address'],server['port'],MANAGER_SERVICE["protocol"],
                                  path='drs/api/manager/services/get/'+id)
        else:
             service = None
        return  service
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        serviceID = request.GET.get('id')
        service  = self.getServiceByID(serviceID)
        print(service)
        stext = str(service)
        stext = stext.replace(",",",\n")
        response =render(request,'userpages/serviceDetails.html',{"error":error_message, 
                                                                 "s": service,
                                                                 "sertxt":stext
                                                                 })
        
        return response        
    def post(self, request, *args, **kwargs):
        return self.get(request)
    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)


#delete container
@login_required
def deleteService(request):
    id = request.GET.get("id")
    server = get_microservice_address_port(MANAGER_SERVICE["name"])
    url = MANAGER_SERVICE["protocol"]+"://"+server['address']+":"+str(server['port'])+"/drs/api/manager/services/delete/"+str(id)
    respo = sendDeleteRequest(json = None,adress=url,username=MANAGER_SERVICE["username"], password=MANAGER_SERVICE["password"])
    if(respo["response"]==200):
        return redirect(WEB_PATH+f"/service/manager?done= Serviço  Apagado Com sucesso")
    else:
         return redirect(WEB_PATH+f"/service/create?error= Erro {str(respo)}")


#manage services
@method_decorator(login_required, name='dispatch')
class  manageServices(View):
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        done = request.GET.get('done')
        ss =  getServices()
        return render(request,"userpages/manageServices.html",{"error":error_message, 
                                                              "done":done,
                                                              "services":ss
                                                    })
    def post(self, request, *args, **kwargs):
        return self.get(request)
    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)


#create service
#createService
@method_decorator(login_required, name='dispatch')
class  createService(View):
    
    def createNewService(self,s):
        server = get_microservice_address_port(MANAGER_SERVICE["name"])
        url = MANAGER_SERVICE["protocol"]+"://"+server['address']+":"+str(server['port'])+"/drs/api/manager/service/create"
        respo = sendPostRequest(json = s,adress=url
                                ,username=MANAGER_SERVICE["username"], password=MANAGER_SERVICE["password"])
        return respo
    
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        done = request.GET.get('done')
        return render(request,"userpages/createService.html",{"error":error_message, 
                                                              "done":done,
                                                    })
    def post(self, request, *args, **kwargs):
        service = request.POST.get("servicejson")
        if(len(service)==0):
            return redirect(WEB_PATH+"/service/create?error=Algum Campo não foi preenchido")
        try:
            s = json.loads(service)
        except Exception as e:
            return redirect(WEB_PATH+"/service/create?error=Existe Algum erro no objecto Json")
        try:
            sname = s["Name"]
            if(serviceNameExists(sname)):
                return redirect(WEB_PATH+"/service/create?error=Já existe um Serviço com esse nome em um Failover")
        except Exception as e:
            pass

        respo = self.createNewService(s)
        if(respo["response"]==201):
            return redirect(WEB_PATH+f"/service/manager?done= Serviço  criado com Sucesso")
        else:
            return redirect(WEB_PATH+f"/service/create?error= Erro {str(respo)}")

        return JsonResponse(respo)
    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)


#manage nw

@method_decorator(login_required, name='dispatch')
class  manageNetworks(View):

    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        done = request.GET.get('done')
        networks =  getNets()
  
        return render(request,"userpages/manageNetworks.html",{"error":error_message, 
                                                              "done":done,
                                                              "networks":networks
                                                    })
    def post(self, request, *args, **kwargs):
        return self.get(request)
    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)



#newNetwork
@method_decorator(login_required, name='dispatch')
class  newNetwork(View):
    
    def createNet(self,data):
        server = get_microservice_address_port(MANAGER_SERVICE["name"])
        url = MANAGER_SERVICE["protocol"]+"://"+server['address']+":"+str(server['port'])+"/drs/api/manager/networks/create"
        respo = sendPostRequest(json = data,adress=url
                                ,username=MANAGER_SERVICE["username"], password=MANAGER_SERVICE["password"])
        return respo
    
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        return render(request,"userpages/criateNetwork.html",{"error":error_message, 
                                                    })
    def post(self, request, *args, **kwargs):
        nome =  request.POST.get("nome")
        net =  request.POST.get("net")
        gateway =  request.POST.get("gateway")
        if(len(nome)==0 or len(net)==0 or len(gateway)==0):
            return redirect(WEB_PATH+"/network/create?error=Algum Campo não foi preenchido")
        
        net =  {
            "nome":nome,
            "rede":net,
            "gateway":gateway 
            }
        
        res= self.createNet(net)
        
        if(res["response"]==201):
            return redirect(WEB_PATH+f"/networks/manager?done= Rede {nome} criada com Sucesso")
        else:
            return redirect(WEB_PATH+f"/network/create?error= Erro {str(res)}")
        return self.get(request)
    def put(self, request, *args, **kwargs):
        return self.get(request)
    def delete(self, request, *args, **kwargs):
        return self.get(request)



#create databse
@method_decorator(login_required, name='dispatch')
class  newContainerDB(View):
    def createDB(self,container):
        server = get_microservice_address_port(BACKUP_SERVICE["name"])
        url = BACKUP_SERVICE["protocol"]+"://"+server['address']+":"+str(server['port'])+"/drs/api/backup/containedb/create"
        respo = sendPostRequest(json = container,adress=url
                                ,username=BACKUP_SERVICE["username"], password=BACKUP_SERVICE["password"])
        return respo
        
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        volumes =  getVolumes()
        images = getAvailableImages()
        try:
            volumes = volumes["Volumes"]
        except Exception as e:
            pass
        return render(request,'userpages/createContainerDB.html',{"error":error_message,
                                                                   "volumes":volumes,
                                                                   "images":images})
    def post(self, request, *args, **kwargs):
        #pegar todos os dados da dashboard
        name = request.POST['containername']
        dir = request.POST["dir"]
        db_image = request.POST["dbimage"]
        volume = request.POST["volume"]
        
        if(len(name)==0 or len(dir)==0 or len(db_image)==0 
           or len(volume)==0 ):
            return redirect(WEB_PATH+"/containerdb/create?error=Algum Campo não foi preenchido")
        im = getImage(db_image)
        if im == None:
                #imagem nao disponivel
                return redirect(WEB_PATH+"/containerdb/create?error=A imagem não Existe")
            
        #cria o container de database
        username = request.POST['username_cc']
        password = request.POST['password_cc']
        hostname = request.POST['hostname_cc']
        container = {
            "name":name,
            "volume":volume,
            "dir":dir,
            "dbimage":db_image,
            "hostname":hostname,
            "username":username,
            "password":password   
        }
        res  = self.createDB(container)
        
        #cria a base de dados do container
        if(res["response"]==204):
            return redirect(WEB_PATH+f"/container/manager?done= Base de Dados {name} criada com Sucesso")
        else:
            return redirect(WEB_PATH+f"/containerdb/create?error= Erro {str(res)}")
        self.get(request)
    def put(self, request, *args, **kwargs):
        return self.get(request)

    def delete(self, request, *args, **kwargs):
        return self.get(request)  
    



#create sincronizer
@method_decorator(login_required, name='dispatch')
class  newDBSincronizer(View):
    def createRsyncContainer(self,container):
        server = get_microservice_address_port(BACKUP_SERVICE["name"])
        url = BACKUP_SERVICE["protocol"]+"://"+server['address']+":"+str(server['port'])+"/drs/api/backup/containerrsync/create"
        respo = sendPostRequest(json = container,adress=url
                                ,username=BACKUP_SERVICE["username"], password=BACKUP_SERVICE["password"])
        return respo
        
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        volumes =  getVolumes()
        images = getAvailableImages()
        try:
            volumes = volumes["Volumes"]
        except Exception as e:
            pass
        return render(request,'userpages/createDatabaseRepl.html',{"error":error_message,
                                                                   "volumes":volumes,
                                                                   "images":images})
    def post(self, request, *args, **kwargs):
        #pegar todos os dados da dashboard
        name = request.POST['name_cc']
        username = request.POST['username_cc']
        password = request.POST['password_cc']
        hostname = request.POST['hostname_cc']
        volume = request.POST["volume"]
        #name_containerdb = request.POST["name_cndb"]
        #db_image = request.POST["dbimage"]
        #or len(name_containerdb)==0 or len(db_image)==0
        if(len(name)==0 or len(username)==0 or len(password)==0 
           or len(hostname)==0 or len(volume)==0 ):
            return redirect(WEB_PATH+"/containerdb/create?error=Algum Campo não foi preenchido")
        #im = self.getImage(db_image)
        #if im == None:
                #imagem nao disponivel
        #        return redirect(WEB_PATH+"/containerdb/create?error=A imagem não Existe")
        #cria o container de sincronizacao
        container = {
            "name":name,
            "volume":volume ,
            "hostname":hostname,
            "username":username,
            "password":password
            }

        res  = self.createRsyncContainer(container)
        
        print(res)
        #cria a base de dados do container
        if(res["response"]==204):
            return redirect(WEB_PATH+f"/container/manager?done= Container {name} criado com Sucesso")
        else:
            return redirect(WEB_PATH+f"/containerdb/create?error= Erro {str(res)}")
        self.get(request)
    def put(self, request, *args, **kwargs):
        return self.get(request)

    def delete(self, request, *args, **kwargs):
        return self.get(request)  
    

#manage volumes
#manageVolumes
@method_decorator(login_required, name='dispatch')
class  manageVolumes(View):
    
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        done = request.GET.get('done')
        volumes = getVolumes()
        #print(volumes)
        try:
            volumes = volumes["Volumes"]
        except Exception as e:
            pass
        return render(request,"userpages/manageVolumes.html",{"error":error_message, 
                                                              "done":done,
                                                              "volumes":volumes
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
        if(len(nome)==0 or len(label)==0):
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
                                                                 "server": server,
                                                                 "specs":getStatusByID(serverID)})
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
        return redirect(WEB_PATH+f"/service/create?done=Imagem {image['nome']} guardada no Registrador, Crie um Serviço para esta imagem")
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

#delete container
@login_required
def deleteContainer(request):
    id = request.GET.get("id")
    serverImage = get_microservice_address_port(IMAGE_SERVICE["name"])
    url = IMAGE_SERVICE["protocol"]+"://"+serverImage['address']+":"+str(serverImage['port'])+"/drs/api/image/container/delete/"+str(id)
    respo = sendDeleteRequest(None,adress=url,username=IMAGE_SERVICE["username"], password=IMAGE_SERVICE["password"])
    if(respo["response"]==204):
         return redirect(WEB_PATH+"/container/manager?done= Container Apagado com Sucesso")
    else:
        return redirect(WEB_PATH+f"/container/manager?error={respo['response']}")
#pause container
def pauseContainer(request):
    id = request.GET.get("id")
    serverImage = get_microservice_address_port(IMAGE_SERVICE["name"])
    url = IMAGE_SERVICE["protocol"]+"://"+serverImage['address']+":"+str(serverImage['port'])+"/drs/api/image/container/pause/"+str(id)
    respo = sendPostRequest(None,adress=url,username=IMAGE_SERVICE["username"], password=IMAGE_SERVICE["password"])
    if(respo["response"]==204):
         return redirect(WEB_PATH+"/container/manager?done= Container Pausado com Sucesso")
    else:
        return redirect(WEB_PATH+f"/container/manager?error={respo['response']}")
#unpause container
def unpauseContainer(request):
    id = request.GET.get("id")
    serverImage = get_microservice_address_port(IMAGE_SERVICE["name"])
    url = IMAGE_SERVICE["protocol"]+"://"+serverImage['address']+":"+str(serverImage['port'])+"/drs/api/image/container/unpause/"+str(id)
    respo = sendPostRequest(None,adress=url,username=IMAGE_SERVICE["username"], password=IMAGE_SERVICE["password"])
    if(respo["response"]==204):
         return redirect(WEB_PATH+"/container/manager?done= Container Iniciado com Sucesso")
    else:
        return redirect(WEB_PATH+f"/container/manager?error={respo['response']}")


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
        done = request.GET.get('done')
        containers =  self.getAvailableContainers()
        return render(request,'userpages/manageContainers.html',{"error":error_message, "containers": containers,"done":done})
    def post(self, request, *args, **kwargs):
        return ""
    def put(self, request, *args, **kwargs):
        return ""
    def delete(self, request, *args, **kwargs):
        return ""


#create Container
@method_decorator(login_required, name='dispatch')
class  newContainer(View):
    
    
    def get(self, request, *args, **kwargs):
        error_message = request.GET.get('error')
        #pegar as imagens disponiveis
        self.imagesAvailable = getAvailableImages()
        return render(request,'userpages/createContainer.html',{"error":error_message, "imageslist": self.imagesAvailable})
    def post(self, request, *args, **kwargs):
        name = request.POST['name_cc']
        username = request.POST['username_cc']
        password = request.POST['password_cc']
        hostname = request.POST['hostname_cc']
        image = request.POST['image_cc']
        print(password)
        try:
            im = getImage(image)
            if im == None:
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
    


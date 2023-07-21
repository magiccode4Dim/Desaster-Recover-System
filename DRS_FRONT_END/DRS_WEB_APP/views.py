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


WEB_PATH = '/web'

IMAGE_SERVICE = {
    "name" : 'IMAGE_SERVICE',
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
    


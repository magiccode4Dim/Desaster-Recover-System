from django.urls import path,include
from DRS_WEB_APP.views import *
from .modulos.gestaodeusuarios import userManagerUrls


urlpatterns = [
#GESTÃO DE USUARIOS
    #dashboard
    path('', dashBoard, name='dashboard')
  
]+userManagerUrls.urlUserManager
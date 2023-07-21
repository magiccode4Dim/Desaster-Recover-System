from django.urls import path,include
from DRS_WEB_APP.views import *
from .modulos.gestaodeusuarios import userManagerUrls


urlpatterns = [
    #dashboard
    path('', dashBoard, name='dashboard'),
    #criar container
    path('container/create', newContainer.as_view(), name='newcontainer')
#GESTÃO DE USUARIOS  newcontainer
]+userManagerUrls.urlUserManager
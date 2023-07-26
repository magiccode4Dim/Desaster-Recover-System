from django.urls import path,include
from DRS_WEB_APP.views import *
from .modulos.gestaodeusuarios import userManagerUrls


urlpatterns = [
    #dashboard
    path('', dashBoard, name='dashboard'),
    #criar container
    path('container/create', newContainer.as_view(), name='newcontainer'),
    #manage containers
    path('container/manager', manageContainers.as_view(), name='managecontainers'),
    #containerDetails
    path('container/details', containerDetails.as_view(), name='containerdetails'),
    #save container as image
    path('container/saveasimage', saveContainerasImage.as_view(), name='containerasimage'),
    #push image
    path('container/push', pushImage.as_view(), name='pushimage')
#GESTÃO DE USUARIOS  newcontainer
]+userManagerUrls.urlUserManager
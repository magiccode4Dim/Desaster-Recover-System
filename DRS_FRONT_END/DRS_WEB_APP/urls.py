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
    path('container/push', pushImage.as_view(), name='pushimage'),
    #create server
    path('server/create', createServer.as_view(), name='createserver'),
    #manage servers
    path('server/manager', manageServers.as_view(), name='manageservers'),
    #server details
    path('server/details', serverDetails.as_view(), name='serverdetails'),
    #create volume
    path('volumes/create', newVolume.as_view(), name='newvolume'),
    #manage volumes
    path('volumes/manager', manageVolumes.as_view(), name='managevolumes'),
    #create sincronizer
    path('sincronizer/create', newDBSincronizer.as_view(), name='newsincronizerdb'),
    #database container
    path('containerdb/create', newContainerDB.as_view(), name='newcontainerdb'),
    #create network
    path('network/create', newNetwork.as_view(), name='newnetwork'),
    #manage networks
    path('networks/manager', manageNetworks.as_view(), name='networkman'),
    #create service
    path('service/create', createService.as_view(), name='newservice'),
    #manage service
    path('service/manager', manageServices.as_view(), name='manageservices'),
    #
#GESTÃO DE USUARIOS  newcontainer
]+userManagerUrls.urlUserManager
from django.urls import path,include
from DRS_GATEWAY_API.views import StatusService,getlaststatusServer,downloadFiles


urlpatterns = [
    #Status Service
    path('statusservice/sendstatus', StatusService.as_view(), name='statusservice'),
    path('statusservice/getlaststatus', getlaststatusServer, name='laststatus'),
    path('downloads', downloadFiles, name='downloadfiles'),

]
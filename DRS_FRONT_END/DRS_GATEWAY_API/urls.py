from django.urls import path,include
from DRS_GATEWAY_API.views import Example


urlpatterns = [
    path('example/', Example.as_view(), name='Example'), 
]
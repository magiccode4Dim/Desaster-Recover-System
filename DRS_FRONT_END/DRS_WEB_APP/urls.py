from django.urls import path,include
from DRS_WEB_APP.views import Login


urlpatterns = [
    path('login/', Login.as_view(), name='Login'), 
]
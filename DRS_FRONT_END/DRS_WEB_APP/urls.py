from django.urls import path,include
from DRS_WEB_APP.views import dashBoard,logOut
from django.contrib.auth import views as auth_views

urlpatterns = [
    #dashboard
    path('', dashBoard, name='dashboard'),
    #Login
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/',logOut , name='logout'),
    
    #   User registration
   
]
from django.urls import path,include
from .userManagerViews import *
from django.contrib.auth import views as auth_views
import os 

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES_AUTH = os.path.join(PROJECT_DIR, 'gestaodeusuarios/')


#TEMPLATES_AUTH = './DRS_WEB_APP/templates/'

urlUserManager= [
#GESTÃO DE USUARIOS
    #dashboard
    #Login
    path('login/', auth_views.LoginView.as_view(
        template_name=os.path.join(TEMPLATES_AUTH, 'templates/login.html'),
        ), name='login'),
    path('logout/',logOut , name='logout'),
    path('register/', register.as_view(), name='register'),
    #   Password Change
    path('password_change/', change_password.as_view(), name='password_change'),
    #   password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name=os.path.join(TEMPLATES_AUTH, 'templates/password_reset_form.html'),
        email_template_name=os.path.join(TEMPLATES_AUTH, 'templates/password_reset_email.html'),
        subject_template_name=os.path.join(TEMPLATES_AUTH, 'templates/password_reset_subject.txt')
        ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name=os.path.join(TEMPLATES_AUTH, 'templates/password_reset_done.html'),
        ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name=os.path.join(TEMPLATES_AUTH, 'templates/password_reset_confirm.html'),
        ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name=os.path.join(TEMPLATES_AUTH, 'templates/password_reset_complete.html'),
        ), name='password_reset_complete'),

    
]
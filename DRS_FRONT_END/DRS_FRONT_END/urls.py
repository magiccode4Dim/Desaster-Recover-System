"""DRS_FRONT_END URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LoginView
from DRS_WEB_APP.views import redirect_login


urlpatterns = [
    path('', redirect_login, name='login'),
    path('web/', include('DRS_WEB_APP.urls')),
    path('api/', include('DRS_GATEWAY_API.urls')),
    path('admin/', admin.site.urls),
]

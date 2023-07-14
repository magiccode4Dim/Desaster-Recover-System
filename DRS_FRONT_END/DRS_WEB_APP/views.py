from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User


#Login
#redirect to login
def redirect_login(request):
    return redirect('/web/login')


@login_required
def dashBoard(request):
    return render(request,'userpages/dashboard.html',{'user':request.user})


from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

#Login
@login_required
def dashBoard(request):
    return render(request,'userpages/dashboard.html')

#Logout
@login_required
def logOut(request):
    logout(request)
    return render(request,'registration/logout.html')
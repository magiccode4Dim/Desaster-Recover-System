from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

# Create your views here.
#Login
class Example(View):
    def get(self, request):
        return HttpResponse("Hello, World!")

    def post(self, request):
        name = request.POST.get('name')
        password =  request.POST.get('passw')
        return HttpResponse(f"Hello, {name}!")
    
    def put(self, request):
        return HttpResponse("This is a PUT request.")

    def delete(self, request):
        return HttpResponse("This is a DELETE request.")
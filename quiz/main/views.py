from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .import models 

class ModelsListView(ListView):
    model = models.Books
    template_name = 'models.html'
    context_object_name = 'dooks'

class UsersAuthView(ListView):
    model = models.Users
    template_name = 'login.html'
    context_object_name = 'login'

def CheckAuth(request, pk):
    login = login.get(pk = pk)
    if request.Post([f'choice_{login.pk}']):
        return HttpResponse("Correct")
    else:
        return HttpResponse("Incorrect")          
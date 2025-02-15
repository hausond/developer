from django.shortcuts import render
from django.http import *
from models import *
from django.core.serializers.json import *

def cities(request: HttpRequest):
    if request.method == 'GET':
        ...
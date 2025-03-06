from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from django.views.decorators.http import require_http_methods
from .models import Quote, Tag, Category
import json
from random import choice

@require_http_methods(["GET"])
def all_tags(request):
    tags = Tag.objects.all()
    tags_json = serialize('json', tags)
    return JsonResponse(tags_json, safe=False)

@require_http_methods(["GET"])
def all_categories(request):
    categories = Category.objects.all()
    categories_json = serialize('json', categories)
    return JsonResponse(categories_json, safe=False)

@require_http_methods(["GET"])
def all_quotes(request):
    quotes = Quote.objects.all()
    quotes_json = serialize('json', quotes)
    return JsonResponse(quotes_json, safe=False)

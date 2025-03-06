from django.http import JsonResponse
from django.urls import reverse
from .models import Quote, Tag, Category
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def all_tags(request):
    tags = list(Tag.objects.values())
    return JsonResponse({
        "data": tags,
        "links": {
            "self": request.build_absolute_uri(),
            "rel": request.build_absolute_uri(reverse('all_data'))
        }
    })

@require_http_methods(["GET"])
def all_categories(request):
    categories = list(Category.objects.values())
    return JsonResponse({
        "data": categories,
        "links": {
            "self": request.build_absolute_uri(),
            "rel": request.build_absolute_uri(reverse('all_data'))
        }
    })

@require_http_methods(["GET"])
def all_quotes(request):
    quotes = list(Quote.objects.values())
    return JsonResponse({
        "data": quotes,
        "links": {
            "self": request.build_absolute_uri(),
            "rel": request.build_absolute_uri(reverse('all_data'))
        }
    })

@require_http_methods(["GET"])
def all_data(request):
    return JsonResponse({
        "data": {
            "tags": list(Tag.objects.values()),
            "categories": list(Category.objects.values()),
            "quotes": list(Quote.objects.values())
        },
        "links": {
            "self": request.build_absolute_uri(),
            "rel": {
                "tags": request.build_absolute_uri(reverse('all_tags')),
                "categories": request.build_absolute_uri(reverse('all_categories')),
                "quotes": request.build_absolute_uri(reverse('all_quotes'))
            }
        }
    })
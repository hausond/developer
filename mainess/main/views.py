from django.http import JsonResponse
from django.urls import reverse
from .models import Quote, Tag, Category
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

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
@csrf_exempt
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

from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse
from .models import Quote, Tag, Category
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["GET", "POST"])
@csrf_exempt
def add_new_quote(request):
    if request.method == 'GET':
        return JsonResponse({
            "message": "Please send a POST request with JSON data to add a new quote",
            "example": {
                "text": "Your quote here",
                "categories": ["optional", "category", "names"],
                "tags": ["optional", "tag", "names"]
            },
            "required_fields": ["text"],
            "links": {
                "all_quotes": request.build_absolute_uri(reverse('all_quotes')),
                "all_categories": request.build_absolute_uri(reverse('all_categories')),
                "all_tags": request.build_absolute_uri(reverse('all_tags'))
            }
        })
    
    # POST request handling
    try:
        # Parse JSON data
        data = json.loads(request.body)
        
        # Validate required fields
        if not data.get('text'):
            return JsonResponse({
                "error": "Validation Error",
                "message": "Quote text is required",
                "required_fields": ["text"]
            }, status=400)
        
        # Create the quote
        quote = Quote.objects.create(text=data['text'])
        
        # Process categories if provided
        if 'categories' in data and isinstance(data['categories'], list):
            for category_name in data['categories']:
                if category_name:  # Skip empty names
                    category, created = Category.objects.get_or_create(
                        name=category_name.strip()
                    )
                    quote.categories.add(category)
        
        # Process tags if provided
        if 'tags' in data and isinstance(data['tags'], list):
            for tag_name in data['tags']:
                if tag_name:  # Skip empty names
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name.strip()
                    )
                    quote.tags.add(tag)
        
        # Prepare response data
        response_data = {
            "status": "success",
            "message": "Quote created successfully",
            "data": {
                "id": quote.id,
                "text": quote.text,
                "categories": [c.name for c in quote.categories.all()],
                "tags": [t.name for t in quote.tags.all()],
                "created_at": quote.id  # Using id as proxy for creation time
            },
            "links": {
                "self": request.build_absolute_uri(),
                "all_quotes": request.build_absolute_uri(reverse('all_quotes')),
                "view_quote": request.build_absolute_uri(reverse('all_quotes')) + f"?id={quote.id}"
            }
        }
        
        return JsonResponse(response_data, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON",
            "message": "The request body contains invalid JSON data"
        }, status=400)
    except Exception as e:
        return JsonResponse({
            "error": "Server Error",
            "message": f"An error occurred while processing your request: {str(e)}"
        }, status=500)
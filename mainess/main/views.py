from django.http import JsonResponse
from django.urls import reverse
from .models import Quote, Tag, Category
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, FieldError
import json


def serialize_tag(tag):
    return {
        "id": tag.id,
        "name": tag.name
    }


def serialize_category(category):
    return {
        "id": category.id,
        "name": category.name
    }


def serialize_quote(quote):
    return {
        "id": quote.id,
        "text": quote.text,
        "tags": [serialize_tag(tag) for tag in quote.tags.all()],
        "categories": [serialize_category(cat) for cat in quote.categories.all()]
    }


@require_http_methods(["GET"])
def all_tags(request):
    sort_by = request.GET.get("sort_by", "id")
    tags = Tag.objects.all()

    try:
        tags = tags.order_by(sort_by)
    except FieldError:
        return JsonResponse({
            "error": "Invalid sort field",
            "message": f"Field '{sort_by}' does not exist on model."
        }, status=400)

    tags_data = [serialize_tag(tag) for tag in tags]

    return JsonResponse({
        "data": tags_data,
        "filters": {"sort_by": sort_by},
        "links": {
            "self": request.build_absolute_uri(),
            "rel": request.build_absolute_uri(reverse('all_quotes'))
        }
    })


@require_http_methods(["GET"])
def all_categories(request):
    sort_by = request.GET.get("sort_by", "id")
    categories = Category.objects.all()

    try:
        categories = categories.order_by(sort_by)
    except FieldError:
        return JsonResponse({
            "error": "Invalid sort field",
            "message": f"Field '{sort_by}' does not exist on model."
        }, status=400)

    categories_data = [serialize_category(cat) for cat in categories]

    return JsonResponse({
        "data": categories_data,
        "filters": {"sort_by": sort_by},
        "links": {
            "self": request.build_absolute_uri(),
            "rel": request.build_absolute_uri(reverse('all_quotes'))
        }
    })


@require_http_methods(["GET", "POST", "PUT", "DELETE"])
@csrf_exempt
def all_quotes(request):
    if request.method == "GET":

        quote_id = request.GET.get("id")
        tag = request.GET.get("tag")
        category = request.GET.get("category")
        sort_by = request.GET.get("sort_by", "id")
        limit = int(request.GET.get("limit", 0))
        offset = int(request.GET.get("offset", 0))

        quotes = Quote.objects.all()

        if quote_id:
            quotes = quotes.filter(id=quote_id)

        if tag:
            quotes = quotes.filter(tags__name__iexact=tag)

        if category:
            quotes = quotes.filter(categories__name__iexact=category)

        try:
            quotes = quotes.order_by(sort_by)
        except FieldError:
            return JsonResponse({
                "error": "Invalid sort field",
                "message": f"Field '{sort_by}' does not exist on model."
            }, status=400)

        if limit > 0:
            quotes = quotes[offset:offset + limit]
        else:
            quotes = quotes[offset:]

        quotes_data = [serialize_quote(q) for q in quotes]

        return JsonResponse({
            "data": quotes_data,
            "filters": {
                "id": quote_id,
                "tag": tag,
                "category": category,
                "sort_by": sort_by,
                "limit": limit,
                "offset": offset
            },
            "links": {
                "self": request.build_absolute_uri(),
                "rel": {
                    "tags": request.build_absolute_uri(reverse('all_tags')),
                    "categories": request.build_absolute_uri(reverse('all_categories')),
                }
            }
        })

    elif request.method == "POST":
        try:
            data = json.loads(request.body)

            if not data.get("text"):
                return JsonResponse({
                    "error": "Validation Error",
                    "message": "Quote text is required"
                }, status=400)

            quote = Quote.objects.create(text=data["text"])

            if "categories" in data and isinstance(data["categories"], list):
                for cat_name in data["categories"]:
                    category, _ = Category.objects.get_or_create(name=cat_name.strip())
                    quote.categories.add(category)

            if "tags" in data and isinstance(data["tags"], list):
                for tag_name in data["tags"]:
                    tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                    quote.tags.add(tag)

            return JsonResponse({
                "status": "success",
                "message": "Quote created successfully",
                "data": serialize_quote(quote),
                "links": {
                    "self": request.build_absolute_uri(),
                    "view_all": request.build_absolute_uri(reverse('all_quotes')),
                    "edit": request.build_absolute_uri() + f"?id={quote.id}",
                    "delete": request.build_absolute_uri() + f"?id={quote.id}"
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON",
                "message": "Request body contains invalid JSON"
            }, status=400)

    elif request.method == "PUT":
        try:
            quote_id = request.GET.get("id")
            if not quote_id:
                return JsonResponse({
                    "error": "Missing ID",
                    "message": "You must provide an 'id' parameter to update a quote"
                }, status=400)

            try:
                quote = Quote.objects.get(id=quote_id)
            except Quote.DoesNotExist:
                return JsonResponse({
                    "error": "Not Found",
                    "message": "Quote with this ID does not exist"
                }, status=404)

            data = json.loads(request.body)

            if "text" in data:
                quote.text = data["text"]

            if "categories" in data and isinstance(data["categories"], list):
                quote.categories.clear()
                for cat_name in data["categories"]:
                    category, _ = Category.objects.get_or_create(name=cat_name.strip())
                    quote.categories.add(category)

            if "tags" in data and isinstance(data["tags"], list):
                quote.tags.clear()
                for tag_name in data["tags"]:
                    tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                    quote.tags.add(tag)

            quote.save()

            return JsonResponse({
                "status": "success",
                "message": "Quote updated successfully",
                "data": serialize_quote(quote),
                "links": {
                    "self": request.build_absolute_uri(),
                    "view_all": request.build_absolute_uri(reverse('all_quotes')),
                    "delete": request.build_absolute_uri() + f"?id={quote.id}"
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({
                "error": "Invalid JSON",
                "message": "Request body contains invalid JSON"
            }, status=400)

    elif request.method == "DELETE":
        quote_id = request.GET.get("id")
        if not quote_id:
            return JsonResponse({
                "error": "Missing ID",
                "message": "You must provide an 'id' parameter to delete a quote"
            }, status=400)

        try:
            quote = Quote.objects.get(id=quote_id)
            quote.delete()
            return JsonResponse({
                "status": "success",
                "message": "Quote deleted successfully",
                "links": {
                    "self": request.build_absolute_uri(),
                    "view_all": request.build_absolute_uri(reverse('all_quotes'))
                }
            })
        except Quote.DoesNotExist:
            return JsonResponse({
                "error": "Not Found",
                "message": "Quote with this ID does not exist"
            }, status=404)


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
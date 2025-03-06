from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tags/', all_tags, name='all_tags'),
    path('categories/', all_categories, name='all_categories'),
    path('quotes/', all_quotes, name='all_quotes')
]

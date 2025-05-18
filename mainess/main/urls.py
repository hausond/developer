from django.urls import path
from .views import all_tags, all_categories, all_quotes, all_data  # Импортируйте все view

urlpatterns = [
    path('tags/', all_tags, name='all_tags'),          # Имя all_tags
    path('categories/', all_categories, name='all_categories'),  # Имя all_categories
    path('quotes/', all_quotes, name='all_quotes'),    # Имя all_quotes
    path('all-data/', all_data, name='all_data'),      # Имя all_data
]
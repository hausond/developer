from django.contrib import admin
from .models import *

# Регистрация модели Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Поля, которые будут отображаться в списке
    search_fields = ('name',)  # Поля, по которым можно будет искать
    list_per_page = 20  # Количество элементов на странице

# Регистрация модели Tag
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 20

# Регистрация модели Quote
@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'display_categories', 'display_tags')  # Отображение полей
    search_fields = ('text',)  # Поиск по тексту цитаты
    list_filter = ('categories', 'tags')  # Фильтры по категориям и тегам
    list_per_page = 20

    # Метод для отображения категорий в списке
    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    display_categories.short_description = 'Categories'  # Название колонки

    # Метод для отображения тегов в списке
    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    display_tags.short_description = 'Tags'  # Название колонки
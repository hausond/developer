from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.name


class Quote(models.Model):

    text = models.TextField()
    author = models.CharField(max_length=100)
    categories = models.ManyToManyField()
    tags = models.ManyToManyField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return f"{self.author}: {self.text[:50]}..."






"""
GET /quotes/random – Получение случайной цитаты.

GET /quotes/{id} – Получение цитаты по ID.

GET /quotes/tag/{tag} – Получение списка цитат по тегу.

GET /quotes/category/{category} – Получение списка цитат по категории.

POST /quotes/ – Добавление новой цитаты.

PUT /quotes/{id} – Обновление цитаты по ID.

DELETE /quotes/{id} – Удаление цитаты по ID.

GET /tags/ – Получение списка всех тегов.

GET /categories/ – Получение списка всех категорий.

GET /quotes/search/{query}?limit&offset – Поиск цитат по ключевым словам с пагинацией.

Добавленные API для управления тегами и категориями:
POST /tags/ – Добавление нового тега.

PUT /tags/{id} – Обновление тега по ID.

DELETE /tags/{id} – Удаление тега по ID.

POST /categories/ – Добавление новой категории.

PUT /categories/{id} – Обновление категории по ID.

DELETE /categories/{id} – Удаление категории по ID.
"""
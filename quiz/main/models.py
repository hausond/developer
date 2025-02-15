from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=50)  
    birthday = models.DateField()
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name
class Books(models.Model):
    name = models.CharField(max_length=50)
    types = models.CharField(max_length=50)
    author = models.ManyToManyField(Author, blank= False)   
    yearofrelease = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    price = models.IntegerField(default= 1)

    def __str__(self):
        return self.name
class Readers(models.Model):
    fio = models.CharField(max_length=50)
    readers_ticket = models.CharField(max_length=8)
    book_in_use = models.BooleanField()
    debt = models.BooleanField()

    def __str__(self):
        return self.fio

class Rent(models.Model):
    Reader = models.ManyToManyField(Readers, blank= False)
    Book = models.ManyToManyField(Books, blank= False)
    Have = models.BooleanField()

    def __str__(self):
        return self.reader

class Personnel(models.Model):
    fio = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    salary = models.IntegerField(default=1)
    graphic_of_work = models.CharField(max_length=50)

    def __str__(self):
        return self.fio

class Graphic(models.Model):
    Day = models.CharField(max_length=50)
    Personnelity = models.ManyToManyField(Personnel, blank= False)
    Hours_Of_Work = models.IntegerField(default=1)

    def __str__(self):
        return self.Day

class Users(models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=50)

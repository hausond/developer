from django.contrib import admin
from .models import Books, Readers, Rent, Graphic, Personnel, Author, Users

@admin.register(Books)
class MaterialsAdmin(admin.ModelAdmin):
    pass 

@admin.register(Readers)
class ProductAdmin(admin.ModelAdmin):
    pass 

@admin.register(Rent)
class CompanyAdmin(admin.ModelAdmin):
    pass 

@admin.register(Graphic)
class ReleaseAdmin(admin.ModelAdmin):
    pass 

@admin.register(Personnel)
class SpecificationAdmin(admin.ModelAdmin):
    pass  

@admin.register(Author)
class SpecificationAdmin(admin.ModelAdmin):
    pass

@admin.register(Users)
class SpecificationAdmin(admin.ModelAdmin):
    pass 
# Register your models here.
# Register your models here.

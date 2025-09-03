from django.contrib import admin
from .models import Category


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'Slug':('Category_name',)}
    list_display = ('Category_name', 'Slug', 'Description', 'Cat_image')
    search_fields = ('Category_name',)  

admin.site.register(Category, CategoryAdmin)
    
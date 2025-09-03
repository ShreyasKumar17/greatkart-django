from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug':('product_name',)}
    list_editable = ('is_available',)
    list_filter = ('category', 'is_available')
    search_fields = ('product_name', 'category__Category_name')

admin.site.register(Product,ProductAdmin)
from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery
import admin_thumbnails

#ProductGallery Admin
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.StackedInline):
    model = ProductGallery
    extra = 1


# Product admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    list_editable = ('is_available',)
    list_filter = ('category', 'is_available')
    search_fields = ('product_name', 'category__Category_name')
    inlines = [ProductGalleryInline]

# Variation admin
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')

# ReviewRating admin
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'subject', 'review', 'rating', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'created_at', 'rating')
    search_fields = ('subject', 'review', 'user__email', 'product__product_name')


try:
    admin.site.unregister(ReviewRating)
except admin.sites.NotRegistered:
    pass

# Register models
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(ProductGallery)

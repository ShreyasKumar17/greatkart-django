from django.contrib import admin
from .models import Account, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'is_active', 'is_staff')
    search_fields = ('first_name', 'last_name', 'username', 'email')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="30" style="border-radius:50%;" />', obj.profile_picture.url)
        return "No Image"

    thumbnail.short_description = 'Profile Picture'

    list_display = ('thumbnail', 'user', 'city', 'state', 'country')
    list_filter = ('state', 'country')
    search_fields = ('user__first_name', 'user__last_name', 'city', 'state', 'country')

admin.site.register(Account, AccountAdmin)

# users/admin.py
from django.contrib import admin
from .models import UserProfile, AdPreview

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'phone')
    search_fields = ('user__username', 'user__email', 'company_name')

@admin.register(AdPreview)
class AdPreviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'board', 'created_at', 'converted_to_ad')
    list_filter = ('converted_to_ad', 'created_at')
    search_fields = ('user__username', 'board__board_id')
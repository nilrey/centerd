from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['text', 'created_date', 'is_published']
    list_filter = ['created_date', 'is_published']
    search_fields = ['text']
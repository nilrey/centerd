from django.contrib import admin
from .models import Organization

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_date']  # Теперь created_date существует
    list_filter = ['created_date']
    search_fields = ['name']
    date_hierarchy = 'created_date'
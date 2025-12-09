from django.contrib import admin
from .models import Organization, ManagementStructure, LegalDocument


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_date']
    list_filter = ['created_date']
    search_fields = ['name', 'description']
    date_hierarchy = 'created_date'


@admin.register(ManagementStructure)
class ManagementStructureAdmin(admin.ModelAdmin):
    list_display = ['organization', 'position', 'full_name', 'appointment_date']
    list_filter = ['position', 'appointment_date']
    search_fields = ['full_name', 'position', 'organization__name']
    date_hierarchy = 'appointment_date'
    raw_id_fields = ['organization']


@admin.register(LegalDocument)
class LegalDocumentAdmin(admin.ModelAdmin):
    list_display = ['organization', 'document_type', 'title', 'number', 'date']
    list_filter = ['document_type', 'date', 'created_date']
    search_fields = ['title', 'number', 'organization__name']
    date_hierarchy = 'date'
    raw_id_fields = ['organization']
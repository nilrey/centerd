from django.shortcuts import render, get_object_or_404
from .models import Organization

def organization_list(request):
    """Список организаций"""
    organizations = Organization.objects.all()
    return render(request, 'organizations/organization_list.html', {
        'organizations': organizations
    })

def organization_detail(request, pk):
    """Паспорт организации"""
    organization = get_object_or_404(Organization, pk=pk)
    return render(request, 'organizations/organization_detail.html', {
        'organization': organization
    })

def organization_card(request, pk):
    """Краткая карточка организации"""
    organization = get_object_or_404(Organization, pk=pk)
    return render(request, 'organizations/organization_card.html', {
        'organization': organization
    })

def management_structure(request, pk):
    """Структура руководства"""
    organization = get_object_or_404(Organization, pk=pk)
    return render(request, 'organizations/management_structure.html', {
        'organization': organization
    })

def legal_documents(request, pk):
    """Правовые документы"""
    organization = get_object_or_404(Organization, pk=pk)
    return render(request, 'organizations/legal_documents.html', {
        'organization': organization
    })

def information_systems(request, pk):
    """Информационные системы"""
    organization = get_object_or_404(Organization, pk=pk)
    return render(request, 'organizations/information_systems.html', {
        'organization': organization
    })

def contacts(request, pk):
    """Контакты организации"""
    organization = get_object_or_404(Organization, pk=pk)
    return render(request, 'organizations/contacts.html', {
        'organization': organization
    })
from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    """Главная страница"""
    return render(request, 'pages/home.html')

def about_page(request):
    """Страница 'О нас'"""
    return render(request, 'pages/about.html')

def contact_page(request):
    """Страница 'Контакты'"""
    return render(request, 'pages/contact.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Review

def home_page(request):
    """Главная страница с формой отзыва"""
    if request.method == 'POST':
        text = request.POST.get('review_text')
        if text and len(text.strip()) > 0:
            Review.objects.create(text=text.strip())
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('home')
        else:
            messages.error(request, 'Пожалуйста, введите текст отзыва')
    
    # Показываем последние 3 отзыва на главной
    recent_reviews = Review.objects.filter(is_published=True)[:3]
    return render(request, 'pages/home.html', {'recent_reviews': recent_reviews})

def about_page(request):
    """Страница 'О нас'"""
    return render(request, 'pages/about.html')

def contact_page(request):
    """Страница 'Контакты'"""
    return render(request, 'pages/contact.html')

def reviews_page(request):
    """Страница со всеми отзывами"""
    all_reviews = Review.objects.filter(is_published=True)
    return render(request, 'pages/reviews.html', {'all_reviews': all_reviews})

def add_review(request):
    """Отдельная страница для добавления отзыва"""
    if request.method == 'POST':
        text = request.POST.get('review_text')
        if text and len(text.strip()) > 0:
            Review.objects.create(text=text.strip())
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('reviews')
        else:
            messages.error(request, 'Пожалуйста, введите текст отзыва')
    
    return render(request, 'pages/add_review.html')
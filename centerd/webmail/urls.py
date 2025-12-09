from django.urls import path

from .views import inbox_view, mail_connect_view

app_name = 'webmail'

urlpatterns = [
    path('', mail_connect_view, name='connect'),
    path('inbox/', inbox_view, name='inbox'),
]

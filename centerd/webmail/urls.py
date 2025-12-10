from django.urls import path

from .views import (
    inbox_view,
    mail_connect_view,
    message_attachment_view,
    message_detail_view,
)

app_name = 'webmail'

urlpatterns = [
    path('', inbox_view, name='inbox'),
    path('inbox/', inbox_view, name='inbox_alias'),
    path('message/<str:uid>/', message_detail_view, name='message_detail'),
    path('message/<str:uid>/attachment/<str:part_id>/', message_attachment_view, name='message_attachment'),
    path('mail_connect_test/', mail_connect_view, name='connect_test'),
]

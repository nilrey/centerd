from django.urls import path

from .views import (
    compose_view,
    inbox_view,
    mail_connect_view,
    message_attachment_view,
    message_detail_view,
    delete_mail_view,
)

app_name = 'webmail'

urlpatterns = [
    path('', inbox_view, name='inbox'),
    path('inbox/', inbox_view, name='inbox_alias'),
    path('message/<str:uid>/', message_detail_view, name='message_detail'),
    path('message/<str:uid>/attachment/<str:part_id>/', message_attachment_view, name='message_attachment'),
    path('compose/', compose_view, name='compose'),
    path('mail_connect_test/', mail_connect_view, name='connect_test'),
    path('ajax/delete_mails/', delete_mail_view, name='delete_mails'),
]

from django.urls import path

from .views import (
    webftp_upload_view,
    webftp_file_list_view,
    webftp_download_view,
    webftp_file_detail_view,
)

app_name = 'webftp'

urlpatterns = [
    path('upload/', webftp_upload_view, name='upload'),
    path('files/', webftp_file_list_view, name='file_list'),
    path('files/<int:pk>/', webftp_file_detail_view, name='detail'),
    path('files/<int:pk>/download/', webftp_download_view, name='download'),
]

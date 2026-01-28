from django.conf import settings
from django.core.files.storage import FileSystemStorage


webftp_storage = FileSystemStorage(
    location=getattr(settings, 'WEBFTP_STORAGE_ROOT', settings.MEDIA_ROOT),
    base_url=(getattr(settings, 'MEDIA_URL', '/media/') + 'webftp/')
)



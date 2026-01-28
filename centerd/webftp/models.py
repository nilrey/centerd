from django.db import models

from .storage import webftp_storage


class WebFtpFile(models.Model):
    file = models.FileField(
        storage=webftp_storage,
        upload_to='',
        verbose_name='Файл',
    )
    alias = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Псевдоним файла',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание файла',
    )
    original_name = models.CharField(
        max_length=255,
        verbose_name='Оригинальное имя файла',
    )
    extension = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Расширение файла',
    )
    content_type = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='MIME-тип',
    )
    size = models.BigIntegerField(
        null=True,
        verbose_name='Размер файла (байт)',
    )
    allowed_usernames = models.TextField(
        blank=True,
        verbose_name='Пользователи с доступом (логины через запятую)',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения',
    )

    class Meta:
        db_table = 'webftp.webftp_files'
        verbose_name = 'Файл WebFTP'
        verbose_name_plural = 'Файлы WebFTP'

    def __str__(self) -> str:
        return self.alias or self.original_name



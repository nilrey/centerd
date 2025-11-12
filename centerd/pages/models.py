from django.db import models
from django.utils import timezone

class Review(models.Model):
    text = models.TextField('Текст отзыва', max_length=1000)
    created_date = models.DateTimeField('Дата создания', default=timezone.now)
    is_published = models.BooleanField('Опубликован', default=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_date']

    def __str__(self):
        return f'Отзыв от {self.created_date.strftime("%d.%m.%Y %H:%M")}'
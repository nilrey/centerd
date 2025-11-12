from django.db import models 
from django.utils import timezone

class Organization(models.Model):
    name = models.CharField('Название организации', max_length=200)
    description = models.TextField('Описание', blank=True)
    created_date = models.DateTimeField('Дата создания', default=timezone.now)  # Исправлено!
    
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
    
    def __str__(self):
        return self.name

class ManagementStructure(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    # ... структура руководства

class LegalDocument(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    # ... правовые документы
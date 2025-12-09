from django.db import models 
from django.utils import timezone


class Organization(models.Model):
    name = models.CharField('Название организации', max_length=200)
    description = models.TextField('Описание', blank=True)
    created_date = models.DateTimeField('Дата создания', default=timezone.now)
    
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ManagementStructure(models.Model):
    """Структура руководства организации"""
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE,
        related_name='management_structures',
        verbose_name='Организация'
    )
    position = models.CharField('Должность', max_length=200, default='')
    full_name = models.CharField('ФИО', max_length=200, default='')
    appointment_date = models.DateField('Дата назначения', null=True, blank=True)
    order_number = models.CharField('Номер приказа', max_length=100, blank=True)
    phone = models.CharField('Телефон', max_length=50, blank=True)
    email = models.EmailField('Email', blank=True)
    created_date = models.DateTimeField('Дата создания', default=timezone.now)
    
    class Meta:
        verbose_name = 'Руководитель'
        verbose_name_plural = 'Структура руководства'
        ordering = ['position', 'full_name']
    
    def __str__(self):
        return f'{self.position} - {self.full_name}'


class LegalDocument(models.Model):
    """Правовые документы организации"""
    DOCUMENT_TYPES = [
        ('charter', 'Устав'),
        ('regulation', 'Положение'),
        ('order', 'Приказ'),
        ('decree', 'Постановление'),
        ('agreement', 'Договор'),
        ('other', 'Прочее'),
    ]
    
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='legal_documents',
        verbose_name='Организация'
    )
    document_type = models.CharField(
        'Тип документа',
        max_length=50,
        choices=DOCUMENT_TYPES,
        default='other'
    )
    title = models.CharField('Название документа', max_length=500, default='')
    number = models.CharField('Номер документа', max_length=100, blank=True)
    date = models.DateField('Дата документа', null=True, blank=True)
    file = models.FileField(
        'Файл документа',
        upload_to='legal_documents/%Y/%m/%d/',
        blank=True,
        null=True
    )
    description = models.TextField('Описание', blank=True)
    created_date = models.DateTimeField('Дата создания', default=timezone.now)
    
    class Meta:
        verbose_name = 'Правовой документ'
        verbose_name_plural = 'Правовые документы'
        ordering = ['-date', 'title']
    
    def __str__(self):
        return f'{self.get_document_type_display()} - {self.title}'
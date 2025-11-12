from django.urls import path
from . import views

app_name = 'organizations'

urlpatterns = [
    path('', views.organization_list, name='list'),
    path('<int:pk>/', views.organization_detail, name='detail'),
    path('<int:pk>/card/', views.organization_card, name='card'),
    path('<int:pk>/management/', views.management_structure, name='management'),
    path('<int:pk>/documents/', views.legal_documents, name='documents'),
    path('<int:pk>/systems/', views.information_systems, name='systems'),
    path('<int:pk>/contacts/', views.contacts, name='contacts'),
]
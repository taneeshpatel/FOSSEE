"""
URL configuration for the equipment API.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('auth/csrf/', views.ensure_csrf),
    path('auth/register/', views.register),
    path('auth/login/', views.auth_login),
    path('auth/logout/', views.auth_logout),
    path('upload/', views.upload_file),
    path('datasets/', views.dataset_list),
    path('datasets/<int:pk>/', views.dataset_detail),
    path('summary/<int:pk>/', views.summary_detail),
    path('pdf/<int:pk>/', views.download_pdf),
    path('download-app/', views.download_app),
]

"""
URL configuration for Chemical Equipment Parameter Visualizer.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('equipment.urls')),
]

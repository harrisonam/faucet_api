"""
URL configuration for core project.
"""
from django.urls import path, include

urlpatterns = [
    # Include the API URLs
    path('api/', include('fund_app.api.urls')),
]

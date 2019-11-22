# strokeapi/urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from strokeapi import views

urlpatterns = [
    path('predict', views.PredictApiView.as_view(), name='predict-list'),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
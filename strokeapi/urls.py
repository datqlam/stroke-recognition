# strokeapi/urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from strokeapi import views

urlpatterns = [
    path('predict', views.StrokeApiView.as_view(), name='stroke-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
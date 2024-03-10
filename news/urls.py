from django.contrib import admin
from django.urls import path

from .views import index, serp_api, summary_news, ai_news

urlpatterns = [
    path('', index, name="index"),
    path('serp_api/', serp_api, name='serp_api'),
    path('summary_news/', summary_news, name='summary_news'),
    path('ai_news/', ai_news, name='ai_news'),
]
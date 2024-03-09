from django.contrib import admin
from django.urls import path

from .views import index, serp_api, summary_news

urlpatterns = [
    path('', index, name="index"),
    path('serp_api/', serp_api, name='serp_api'),
    path('summary/', summary_news, name='summary'),

]
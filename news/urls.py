from django.contrib import admin
from django.urls import path

from .views import index, serp_api, summary_news,news,news_list

urlpatterns = [
    path('', index, name="index"),
    path('serp_api/', serp_api, name='serp_api'),
    path('summary/', summary_news, name='summary'),
    path('news/',news,name="news"),
    path('list/<str:name>/', news_list, name='news_list'),

]
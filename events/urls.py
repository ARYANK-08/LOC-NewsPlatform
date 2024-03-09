from django.contrib import admin
from django.urls import path

from . import views 

urlpatterns = [
    path('', views.fetchevents, name="index"),
    path('event_details', views.event_details, name='event_details'),
]


from django.contrib import admin
from django.urls import path

from .views import visualise,gemini

urlpatterns = [
    path('visualise', visualise, name="visualise"),
    path('gemini', gemini, name='gemini'),

]
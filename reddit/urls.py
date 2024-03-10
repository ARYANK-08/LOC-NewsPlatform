
   
from django.urls import path
from . import views

urlpatterns = [
    path('sentiment-analysis/', views.sentiment_analysis, name='sentiment_analysis'),
]



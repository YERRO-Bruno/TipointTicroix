from django.contrib import admin
from django.urls import path
from tipoint_ticroix import views
urlpatterns = [
    path('tipointticroix/', views.tipointticroix, name='tipointticroix')
]
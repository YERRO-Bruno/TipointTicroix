
from django.contrib import admin
from django.urls import path
from tipoint_ticroix import views
urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('tipointticroix/', views.tipointticroix, name='tipointticroix'),
    path('tipointticroix/machines/', views.machines, name='machines'),
    path('admin/', admin.site.urls),
]

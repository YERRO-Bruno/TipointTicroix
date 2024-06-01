
from django.contrib import admin
from django.urls import path
from tipoint_ticroix import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('tipointticroix/', views.tipointticroix, name='tipointticroix'),
    path('tipointticroix/machines/', views.machines, name='machines'),
    path('tipointticroix/internet/', views.internet, name='internet'),
    path('tipointticroix/preregister/', views.preregister, name='preregister'),
    path('tipointticroix/register/', views.register, name='register'),
    path('tipointticroix/connect/', views.connect, name='connect'),
    path('tipointticroix/logout/', views.logout_view, name='logout_view'),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

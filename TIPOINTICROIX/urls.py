
from django.contrib import admin
from django.urls import path
from tipoint_ticroix import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('tipointticroix/', views.accueil, name='accueil'),
    path('tipointticroix/jeu', views.tipointticroix, name='tipointticroix'),
    path('tipointticroix/machines/', views.machines, name='machines'),
    path('tipointticroix/internet/', views.internet, name='internet'),
    path('tipointticroix/preregister/', views.preregister, name='preregister'),
    path('tipointticroix/register/', views.register, name='register'),
    path('tipointticroix/connect/', views.connect, name='connect'),
    path('tipointticroix/logout/', views.logout_view, name='logout_view'),
    path('tipointticroix/apropos/', views.apropos, name='apropos'),
    path('tipointticroix/mentions/', views.mentions, name='mentions'),
    path('tipointticroix/statistics/', views.statistics, name='statistics'),
    path('tipointticroix/desinscription/', views.desinscription, name='desinscriptionn'),
    path('admin/', admin.site.urls),
    path("api/userconnecteds",views.api_userconnecteds,name="api_userconnecteds")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

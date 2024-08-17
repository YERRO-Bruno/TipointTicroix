
from django.contrib import admin
from django.urls import path,include
from tipoint_ticroix import views
from django.conf.urls.static import static
from django.conf import settings

# Custom 404 error view
handler404 = views.error_404

urlpatterns = [
    path('', views.accueil, name='home_redirect'),
    path('jeu/', views.tipointticroix, name='jeu'),
    path('machines/', views.machines, name='machines'),
    path('internet/', views.internet, name='internet'),
    path('preregister/', views.preregister, name='preregister'),
    path('register/', views.register, name='register'),
    path('connect/', views.connect, name='connect'),
    path('logout/', views.logout_view, name='logout_view'),
    path('apropos/', views.apropos, name='apropos'),
    path('mentions/', views.mentions, name='mentions'),
    path('statistics/', views.statistics, name='statistics'),
    path('desinscription/', views.desinscription, name='desinscriptionn'),
    path('prepassword/', views.prepassword, name='prepassword'),
    path('modifpassword/', views.modifpassword, name='modifpassword'),
    path('admin/', admin.site.urls),
]
#] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

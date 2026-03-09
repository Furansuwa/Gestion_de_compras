from django.contrib import admin
from django.urls import path, include
from gestion import views  # Importamos nuestras vistas

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Esto activa las rutas de Django: /accounts/login/ y /accounts/logout/
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # Esta será nuestra página de inicio protegida
    path('', views.home, name='home'), 
]
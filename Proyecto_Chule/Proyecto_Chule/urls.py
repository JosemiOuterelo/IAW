"""Proyecto_Chule URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from VayaPajaro.views import *
from VayaPajaro.forms import *
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',TemplateView.as_view(template_name='VayaPajaro/Home.html'),name='Home'),
    url(r'^usuario/registrarse',registrarse,name='Registrarse'),
	url(r'^usuario/login',iniciarsesion,name='Login'),
	url(r'^usuario/logout',cerrarsesion,name='Logout'),
    url(r'^usuario/mostrar_usuarios/',MostrarUsuarios.as_view(),name='Mostrar_Usuarios'),
    url(r'^usuario/modificar/(?P<pk>\d+)',ModificarUsuarios.as_view(),name='Modificar_Usuarios'),
    url(r'^usuario/eliminar/(?P<pk>\d+)',EliminarUsuario.as_view(),name='Eliminar_Usuario'),
]

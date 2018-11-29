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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from VayaPajaro.views import *
from VayaPajaro.forms import *
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',TemplateView.as_view(template_name='VayaPajaro/Home.html')),
    url(r'^usuario/registrarse',registrarse,name='Registrarse'),
	url(r'^usuario/login',iniciarsesion,name='Login'),
	url(r'^usuario/logout',cerrarsesion,name='Logout'),
    url(r'^usuario/mostrar_usuarios/',MostrarUsuarios.as_view(),name='Mostrar_Usuarios'),
    url(r'^usuario/modificar/(?P<pk>\d+)',ModificarUsuarios.as_view(),name='Modificar_Usuarios'),
    url(r'^usuario/eliminar/(?P<pk>\d+)',EliminarUsuario.as_view(),name='Eliminar_Usuario'),
    url(r'^ave/agregar',crearAve,name='CrearAve'),
    url(r'^ave/mostrar_aves/',MostrarAves.as_view(),name='Mostrar_Aves'),
    url(r'^ave/mostrar_ave/(?P<nombre>\w+)/',mostrarave,name="Mostrar_ave"),
    url(r'^ave/modificar/(?P<pk>\d+)',ModificarAves.as_view(),name="Modificar_Ave"),
    url(r'^ave/eliminar/(?P<pk>\d+)',EliminarAve.as_view(),name='Eliminar_Ave'),
    url(r'^articulo/mostrar_articulos/',MostrarArticulos.as_view(),name='Mostrar_Articulos'),
    url(r'^foto/subir/(?P<nombre>\w+)',crearFoto,name='CrearFoto'),
    url(r'^foto/eliminar/(?P<pk>\d+)',eliminarFoto,name="Eliminar_Foto"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

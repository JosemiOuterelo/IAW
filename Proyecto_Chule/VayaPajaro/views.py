# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse

from django.http import Http404,HttpResponseRedirect,HttpResponse,StreamingHttpResponse

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required,user_passes_test

from django.views.generic.edit import UpdateView,DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import datetime                 
from django.contrib.auth.models import User
from VayaPajaro.models import *
from VayaPajaro.forms import *
from VayaPajaro.serializers import *
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Guacamole 

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt,requires_csrf_token
from VayaPajaro import client

import logging
import uuid
import threading


# Create your views here.

# Registro e Iniciar/Cerrar sesion

def registrarse(request):
	if request.method == 'POST':
		form = RegistrarseForm(request.POST,request.FILES)
		if form.is_valid():
			user = form.save()
			user.is_staff = False
			user.refresh_from_db()
			user.usuario.fnacimiento = form.cleaned_data.get('fnacimiento')
			user.usuario.estudios = form.cleaned_data.get('estudios')
			user.usuario.fotoPerfil = form.cleaned_data.get('fotoPerfil')
			user.save()
			password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username,password=password)
			login(request,user)
			return HttpResponseRedirect('/')
	else:
		form = RegistrarseForm()
	return render(request,'VayaPajaro/Registrarse.html',{'form':form})


def iniciarsesion(request):
	if request.method == 'POST':
		form = IniciarSesion(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(request,username=username,password=password)
			if user is not None:
				login(request,user)
				return HttpResponseRedirect('/')
			else:
				return HttpResponse("¡Usuario incorrecto!")
	else:
		form = IniciarSesion()
	return render(request,'VayaPajaro/Login.html',{'form':form})
	
def iniciarsesionadmin(request):
	if request.method == 'POST':
		form = IniciarSesion(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(request,username=username,password=password)
			if user is not None:
				if user.is_staff == True:
					login(request,user)
					return HttpResponseRedirect('/')
				else:
					return HttpResponse("El usuario debe ser administrador.")
			else:
				return HttpResponse("¡Usuario incorrecto!")
	else:
		form = IniciarSesion()
	return render(request,'VayaPajaro/Loginadmin.html',{'form':form})

def cerrarsesion(request):
	logout(request)
	return HttpResponseRedirect('/')

# Usuarios

class MostrarUsuarios(UserPassesTestMixin,ListView):
	model = Usuario
	login_url='/usuario/loginadmin/'
	fields = '__all__'
	template_name = 'VayaPajaro/Mostrar_Usuarios.html'
	
	def get_context_data(self, **kwargs):
		context = super(MostrarUsuarios,self).get_context_data(**kwargs)
		return context
		
	def test_func(self):
		return self.request.user.is_staff == True
		
		
class ModificarUsuarios(UserPassesTestMixin,UpdateView):
	model = Usuario
	login_url='/usuario/loginadmin/'
	fields = '__all__'
	template_name = 'VayaPajaro/Modificar_Usuarios.html'
	success_url = '/usuario/mostrar_usuarios/'
	
	def test_func(self):
		return self.request.user.is_staff == True
	
	
class EliminarUsuario(UserPassesTestMixin,DeleteView):
	model = User
	login_url='/usuario/loginadmin/'
	template_name = 'VayaPajaro/Eliminar_Usuario.html'
	success_url = 'http://127.0.0.1:8000/'
	
	def test_func(self):
		return self.request.user.is_staff == True
		
	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.usuario.fotoPerfil.delete()
		self.object.delete()
		return HttpResponseRedirect(self.get_success_url())


# Aves, Articulos y Fotos

@login_required(login_url='/usuario/login/')
def crearAve(request):
	if request.method == 'POST':
		form1 = CrearAveForm(request.POST,request.FILES)
		formset = crearfotoformset(request.POST,request.FILES)
		if form1.is_valid() and formset.is_valid():
			articulo = Articulo()
			ave = Ave()
			usuario = Usuario.objects.get(user=request.user)
			articulo.usuario = usuario
			ave.nombre = form1.cleaned_data.get('nombre')
			ave.descripcion = form1.cleaned_data.get('descripcion')
			ave.alimentacion = form1.cleaned_data.get('alimentacion')
			ave.habitat = form1.cleaned_data.get('habitat')
			ave.localizacion = form1.cleaned_data.get('habitat')
			ave.save()
			for f in formset.cleaned_data:
				if len(f)>0:
					foto = Foto()
					foto.imagen = f.get('imagen')
					foto.usuario = usuario
					foto.save()
					ave.fotos.add(foto)
			ave.save()
			articulo.ave = ave
			articulo.fcreacion = datetime.datetime.now()
			articulo.save()
			return HttpResponseRedirect('/ave/mostrar_aves/')
	else:
		form1 = CrearAveForm()
		formset = crearfotoformset()
		
	return render(request,'VayaPajaro/CrearAve.html',{'ave':form1,'Imagenes':formset})
	
	
class MostrarAves(LoginRequiredMixin,ListView):
	model = Ave
	fields = '__all__'
	login_url = '/usuario/login/'
	template_name = 'VayaPajaro/Mostrar_Aves.html'
	
	def get_context_data(self, **kwargs):
		context = super(MostrarAves,self).get_context_data(**kwargs)
		mostrar = Ave.objects.all().order_by('nombre')
		context['mostrar'] = mostrar
		return context
		
		
@login_required(login_url='/usuario/login/')
def mostrarave(request,nombre):
	ave = Ave.objects.get(nombre=nombre.replace('_',' '))
	if ave:
		return render(request,'VayaPajaro/Mostrar_ave.html',{'Ave':ave})
	else:
		return HttpResponseRedirect('No existe ave.')
		
class ModificarAves(LoginRequiredMixin,UpdateView):
	model = Ave
	login_url='/usuario/login/'
	fields = ['nombre','descripcion','alimentacion','habitat','localizacion']
	template_name = 'VayaPajaro/Modificar_Aves.html'
	success_url = '/ave/mostrar_aves/'

class EliminarAve(UserPassesTestMixin,DeleteView):
	model = Ave
	login_url='usuario/loginadmin/'
	template_name = 'VayaPajaro/Eliminar_Ave.html'
	success_url = '/ave/mostrar_aves/'
	
	def test_func(self):
		return self.request.user.is_staff == True
		
	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		for imagenes in self.object.fotos.all():
			imagenes.imagen.delete()	
		self.object.fotos.clear()
		self.object.delete()
		return HttpResponseRedirect(self.get_success_url())

class MostrarArticulos(LoginRequiredMixin,ListView):
	model = Articulo
	fields = '__all__'
	login_url = '/usuario/login/'
	template_name = 'VayaPajaro/Mostrar_Articulos.html'
	
	def get_context_data(self, **kwargs):
		context = super(MostrarArticulos,self).get_context_data(**kwargs)
		return context
 
@login_required(login_url='/usuario/login/')
def crearFoto(request,nombre):
	if request.method == 'POST':
		form = CrearFotoForm(request.POST,request.FILES)
		if form.is_valid():
			ave = Ave.objects.get(nombre=nombre.replace('_',' '))
			usuario = Usuario.objects.get(user=request.user)
			imagen = Foto()
			imagen.imagen = form.cleaned_data.get('imagen')
			imagen.usuario = usuario
			imagen.save()
			ave.fotos.add(imagen)
			return HttpResponseRedirect('/ave/mostrar_ave/%s/' % ave.nombre.replace(' ','_'))
	else:
		form = CrearFotoForm()	
	return render(request,'VayaPajaro/CrearFoto.html',{'fotos':form})


def administrador(user):
	return user.is_staff
	
	
@login_required(login_url='/usuario/login/')
def eliminarFoto(request,pk):
	if request.method == 'POST':
		foto = Foto.objects.get(pk=pk)
		ave = foto.ave_set.all()
		nombre= ave[0].nombre
		foto.imagen.delete()
		foto.delete()
		return HttpResponseRedirect('/ave/mostrar_ave/%s/' % nombre.replace(' ','_'))
	return render(request,'VayaPajaro/Eliminar_Foto.html')

#REST API

class SerMostrar_Usuarios(generics.ListCreateAPIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	queryset = Usuario.objects.all()
	serializer_class = UsuarioSerializer
	
class SerMostrar_Aves(generics.ListCreateAPIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	queryset = Ave.objects.all()
	serializer_class = AveSerializer
	
class SerMostrar_Articulos(generics.ListCreateAPIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	queryset = Articulo.objects.all()
	serializer_class = ArticuloSerializer
	
class SerMostrar_Fotos(generics.ListCreateAPIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	queryset = Foto.objects.all()
	serializer_class = FotoSerializer
	
class SerMostrar_Usuario(generics.RetrieveUpdateDestroyAPIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	queryset = Usuario.objects.all()
	serializer_class = UsuarioSerializer
	
class SerMostrar_Ave(generics.RetrieveUpdateDestroyAPIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	queryset = Ave.objects.all()
	serializer_class = AveSerializer
	
class SerMostrar_Articulo(generics.RetrieveUpdateDestroyAPIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	queryset = Articulo.objects.all()
	serializer_class = ArticuloSerializer
	
class SerMostrar_Foto(generics.RetrieveUpdateDestroyAPIView):
	authentication_classes = (SessionAuthentication, BasicAuthentication)
	permission_classes = (IsAuthenticated,)
	queryset = Foto.objects.all()
	serializer_class = FotoSerializer
	

# GUACAMOLE

logger = logging.getLogger(__name__)
sockets = {}
sockets_lock = threading.RLock()
read_lock = threading.RLock()
write_lock = threading.RLock()
pending_read_request = threading.Event()

#@csrf_exempt
#@requires_csrf_token
def index(request):
    return render(request,'Guacamole.html')
#    return render_to_response('Guacamole.html',{},context_instance=RequestContext(request))

@csrf_exempt
def tunnel(request):
    qs = request.META['QUERY_STRING']
    logger.info('tunnel %s', qs)
    if qs == 'connect':
        return _do_connect(request)
    else:
        tokens = qs.split(':')
        if len(tokens) >= 2:
            if tokens[0] == 'read':
                return _do_read(request, tokens[1])
            elif tokens[0] == 'write':
                return _do_write(request, tokens[1])

	return HttpResponse(status=400)


def _do_connect(request):
    # Connect to guacd daemon
	guac = client.GuacamoleClient()
	guac.connect(protocol='ssh',hostname='192.168.100.1',port=22,username='chule',password='beticanos')
#	guac.connect(protocol='vnc',hostname='192.168.100.1',port=5900,password='chule')
	cache_key = str(uuid.uuid4())
	with sockets_lock:
		logger.info('Saving socket with key %s', cache_key)
		sockets[cache_key] = guac

	response = HttpResponse(content=cache_key)
	response['Cache-Control'] = 'no-cache'

	return response


def _do_read(request, cache_key):
    pending_read_request.set()

    def content():
        with sockets_lock:
            guac = sockets[cache_key]

        with read_lock:
            pending_read_request.clear()

            while True:
                content = guac.read()
                if content:
                    yield content
                else:
                    break

                if pending_read_request.is_set():
                    logger.info('Letting another request take over.')
                    break

            # End-of-instruction marker
            yield '0.;'

    response = StreamingHttpResponse(content(),content_type='application/octet-stream')
    response['Cache-Control'] = 'no-cache'
    return response


def _do_write(request, cache_key):
    with sockets_lock:
        guac = sockets[cache_key]

    with write_lock:
        while True:
            chunk = request.read(8192)
            if chunk:
                guac.write(chunk)
            else:
                break

    response = HttpResponse(content_type='application/octet-stream')
    response['Cache-Control'] = 'no-cache'
    return response

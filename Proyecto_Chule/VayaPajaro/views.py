# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import Http404,HttpResponseRedirect,HttpResponse

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import UserPassesTestMixin

from django.views.generic.edit import UpdateView,DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import datetime                 
from django.contrib.auth.models import User
from VayaPajaro.models import *
from VayaPajaro.forms import *

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

def cerrarsesion(request):
	logout(request)
	return HttpResponseRedirect('/')

# Usuarios

def MostrarImagenDePerfil(request):
	foto_perfil = ''
	if request.user.is_authenticated:
		user = User.objects.get(username=request.user.username)
		foto_perfil = user.usuario.fotoPerfil.url
	return render(request,'base.html',{'foto':foto_perfil})

class MostrarUsuarios(UserPassesTestMixin,ListView):
	model = Usuario
	login_url='/usuario/login'
	fields = '__all__'
	template_name = 'VayaPajaro/Mostrar_Usuarios.html'
	
	def get_context_data(self, **kwargs):
		context = super(MostrarUsuarios,self).get_context_data(**kwargs)
		return context
		
	def test_func(self):
		return self.request.user.is_staff == True
		
		
class ModificarUsuarios(UserPassesTestMixin,UpdateView):
	model = Usuario
	login_url='/usuario/login'
	fields = '__all__'
	template_name = 'VayaPajaro/Modificar_Usuarios.html'
	success_url = 'http://127.0.0.1:8000/'
	
	def test_func(self):
		return self.request.user.is_staff == True
	
	
class EliminarUsuario(UserPassesTestMixin,DeleteView):
	model = User
	login_url='/usuario/login'
	template_name = 'VayaPajaro/Eliminar_Usuario.html'
	success_url = 'http://127.0.0.1:8000/'
	
	def test_func(self):
		return self.request.user.is_staff == True


# Aves, Articulos y Fotos

def crearAve(request):
	if request.method == 'POST':
		form1 = CrearAveForm(request.POST,request.FILES)
		if form1.is_valid():
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
			Fotos = form1.cleaned_data.get('fotos')
			for foto in Fotos:
				ave.fotos.add(foto)
			ave.save()
			articulo.ave = ave
			articulo.fcreacion = datetime.datetime.now()
			articulo.save()
			return HttpResponseRedirect('/ave/mostrar_aves/')
	else:
		form1 = CrearAveForm()
		
	return render(request,'VayaPajaro/CrearAve.html',{'ave':form1})
	
	
class MostrarAves(ListView):
	model = Ave
	fields = '__all__'
	template_name = 'VayaPajaro/Mostrar_Aves.html'
	
	def get_context_data(self, **kwargs):
		context = super(MostrarAves,self).get_context_data(**kwargs)
		return context

class EliminarAve(DeleteView):
	model = Ave
	template_name = 'VayaPajaro/Eliminar_Ave.html'
	success_url = 'http://127.0.0.1:8000/'

		
class MostrarArticulos(ListView):
	model = Articulo
	fields = '__all__'
	template_name = 'VayaPajaro/Mostrar_Articulos.html'
	
	def get_context_data(self, **kwargs):
		context = super(MostrarArticulos,self).get_context_data(**kwargs)
		return context
 

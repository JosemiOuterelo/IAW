# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import Http404,HttpResponseRedirect,HttpResponse

from django.contrib.auth import login,logout,authenticate

from django.views.generic.edit import UpdateView,DeleteView
from django.views.generic.list import ListView

from .models import Usuario
from .forms import RegistrarseForm,IniciarSesion

# Create your views here.

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
				return HttpResponse("¡No puede iniciar sesion!")
	else:
		form = IniciarSesion()
	return render(request,'VayaPajaro/Login.html',{'form':form})

def cerrarsesion(request):
	logout(request)
	return HttpResponseRedirect('/usuario/login')

	

class MostrarUsuarios(ListView):
	model = Usuario
	fields = '__all__'
	template_name = 'VayaPajaro/Mostrar_Usuarios.html'
	
	def get_context_data(self, **kwargs):
		context = super(MostrarUsuarios,self).get_context_data(**kwargs)
		return context
		
class ModificarUsuarios(UpdateView):
	model = Usuario
	fields = '__all__'
	template_name = 'VayaPajaro/Modificar_Usuarios.html'
	
class EliminarUsuario(DeleteView):
	model = Usuario
	template_name = 'VayaPajaro/Eliminar_Usuario.html'
	success_url = 'http://127.0.0.1:8000/usuario/mostrar_usuarios/'

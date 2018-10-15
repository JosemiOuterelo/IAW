# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import Http404

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.list import ListView

from .models import Usuario

# Create your views here.

class CrearUsuario(CreateView):
	model = Usuario
	fields = '__all__'
	template_name = 'VayaPajaro/Crear_Usuario.html'

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

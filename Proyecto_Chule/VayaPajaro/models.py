# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Usuario(models.Model):
	nombre = models.CharField(max_length=40)
	nombreCuenta = models.CharField(max_length=40)
	fnacimiento = modelfs.DateField()
	correo = models.CharField(max_length=60,default='Desconocido')
	estudios = models.CharField(max_length=500,default='Desconocidos')
	fotoPerfil = models.ImageField(upload_to='Fotos de Perfil') 
	
	def __unicode__(self):
		return self.nombreCuenta

class Ave(models.Model):
	nombre = models.CharField(max_length=40,default='Desconocido',blank=True,null=True)
	descripcion = models.TextField(max_length=2000,default='Desconocido',blank=True,null=True)
	alimentacion = models.TextField(max_length=2000,default='Desconocida',blank=True,null=True)
	habitat = models.TextField(max_length=2000,default='Desconocida',blank=True,null=True)
	localizacion = models.TextField(max_length=2000,default='Desconocida',blank=True,null=True)
	fotos = models.ManyToManyField(Foto)

	def __unicode__(self):
		return self.nombre
	
class Articulo(models.Model):
	usuario = models.ForeignKey(Usuario)
	ave = models.ForeignKey(Ave, on_delete=models.CASCADE)
	fcreacion = models.DateField()
	
	def __unicode__(self):
		return '%s %d' % (self.usuario,self.ave,self.fcreacion)
		
class Foto(models.Model):
	imagen = models.ImageField(upload_to='Fotos de Aves')
	latitud = models.DecimalField(max_digits=9,decimal_places=6)
	longitud = models.DecimalField(max_digits=9,decimal_places=6)
	
	def __unicode__(self):
		return self.imagen

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Usuario(models.Model):
	user = models.OneToOneField(User,related_name='usuario',on_delete=models.CASCADE,default=None)
	fnacimiento = models.DateField(null=True)
	estudios = models.CharField(max_length=500,default='Desconocidos')
	fotoPerfil = models.ImageField(upload_to='Fotos_de_Perfil') 
	
	def __unicode__(self):
		return self.user.username
		
	def get_absolute_url(self):
		return 'http://127.0.0.1:8000/usuario/mostrar_usuarios/'

@receiver(post_save, sender=User)
def update_user_usuario(sender, instance, created, **kwargs):
	if created:
		Usuario.objects.create(user=instance)
	instance.usuario.save()

class Ave(models.Model):
	nombre = models.CharField(max_length=40,default='Desconocido',blank=True,null=True)
	descripcion = models.TextField(max_length=2000,default='Desconocido',blank=True,null=True)
	alimentacion = models.TextField(max_length=2000,default='Desconocida',blank=True,null=True)
	habitat = models.TextField(max_length=2000,default='Desconocida',blank=True,null=True)
	localizacion = models.TextField(max_length=2000,default='Desconocida',blank=True,null=True)
	fotos = models.ManyToManyField('Foto')

	def __unicode__(self):
		return self.nombre
		
	def mostrar_nombre_con_espacios(self):
		return self.nombre.replace(' ', '_')
	
class Articulo(models.Model):
	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	ave = models.ForeignKey(Ave, on_delete=models.CASCADE)
	fcreacion = models.DateField()
	
	def __unicode__(self):
		return '%s %d' % (self.usuario,self.ave,self.fcreacion)
		
class Foto(models.Model):
	imagen = models.ImageField(upload_to='Fotos_de_Aves')
	
	def __unicode__(self):
		return unicode(self.imagen)

from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.forms import formset_factory,PasswordInput

from django.contrib.auth.models import User

from VayaPajaro.models import *

class RegistrarseForm(UserCreationForm):
	fnacimiento = forms.DateField()
	estudios = forms.CharField(max_length=500)
	fotoPerfil = forms.ImageField() 
	
	class Meta:
		model = User
		fields = ('username','first_name','last_name','email','password1','password2','fnacimiento','estudios','fotoPerfil')

class IniciarSesion(forms.Form):
	username = forms.CharField(max_length=500)
	password = forms.CharField(max_length=500,widget=PasswordInput())

	
class CrearAveForm(forms.Form):
	nombre = forms.CharField(max_length=40)
	descripcion = forms.CharField(max_length=2000,widget=forms.Textarea)
	alimentacion = forms.CharField(max_length=2000,widget=forms.Textarea)
	habitat = forms.CharField(max_length=2000,widget=forms.Textarea)
	localizacion = forms.CharField(max_length=2000,widget=forms.Textarea)	

class CrearFotoForm(forms.Form):
	imagen = forms.ImageField()

crearfotoformset = formset_factory(CrearFotoForm,extra=5)


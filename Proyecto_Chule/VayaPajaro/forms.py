from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

class RegistrarseForm(UserCreationForm):
	fnacimiento = forms.DateField()
	estudios = forms.CharField(max_length=500)
	fotoPerfil = forms.ImageField() 
	
	class Meta:
		model = User
		fields = ('username','first_name','last_name','email','password1','password2','fnacimiento','estudios','fotoPerfil')

class IniciarSesion(forms.Form):
	username = forms.CharField(max_length=500)
	password = forms.CharField(max_length=500)
	

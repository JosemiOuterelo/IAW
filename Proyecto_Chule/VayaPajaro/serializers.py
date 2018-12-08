from rest_framework import serializers
from VayaPajaro.models import *

class UsuarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = Usuario
		fields = '__all__'

class AveSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ave
		fields = '__all__'

class ArticuloSerializer(serializers.ModelSerializer):
	class Meta:
		model = Articulo
		fields = '__all__'
	
		
class FotoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Foto
		fields = '__all__'

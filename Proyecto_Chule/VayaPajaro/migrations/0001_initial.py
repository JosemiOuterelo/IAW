# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-12 12:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fcreacion', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Ave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, default='Desconocido', max_length=40, null=True)),
                ('descripcion', models.TextField(blank=True, default='Desconocido', max_length=2000, null=True)),
                ('alimentacion', models.TextField(blank=True, default='Desconocida', max_length=2000, null=True)),
                ('habitat', models.TextField(blank=True, default='Desconocida', max_length=2000, null=True)),
                ('localizacion', models.TextField(blank=True, default='Desconocida', max_length=2000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='Fotos de Aves')),
                ('latitud', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitud', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('nombreCuenta', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=40)),
                ('fnacimiento', models.DateField()),
                ('correo', models.CharField(default='Desconocido', max_length=60)),
                ('estudios', models.CharField(default='Desconocidos', max_length=500)),
                ('fotoPerfil', models.ImageField(upload_to='Fotos de Perfil')),
            ],
        ),
        migrations.AddField(
            model_name='ave',
            name='fotos',
            field=models.ManyToManyField(to='VayaPajaro.Foto'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='ave',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VayaPajaro.Ave'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VayaPajaro.Usuario'),
        ),
    ]

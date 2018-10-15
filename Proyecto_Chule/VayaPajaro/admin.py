# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Usuario
from .models import Ave
from .models import Articulo
from .models import Foto

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Ave)
admin.site.register(Articulo)
admin.site.register(Foto)


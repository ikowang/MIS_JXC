from django.contrib import admin
from apps.Supplyer.models import Supplyer

# Register your models here.

admin.site.register(Supplyer,admin.ModelAdmin)
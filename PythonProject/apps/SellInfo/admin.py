from django.contrib import admin
from apps.SellInfo.models import SellInfo

# Register your models here.

admin.site.register(SellInfo,admin.ModelAdmin)
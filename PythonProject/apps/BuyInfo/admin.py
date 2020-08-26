from django.contrib import admin
from apps.BuyInfo.models import BuyInfo

# Register your models here.

admin.site.register(BuyInfo,admin.ModelAdmin)
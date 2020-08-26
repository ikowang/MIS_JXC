from django.contrib import admin
from apps.ProductInfo.models import ProductInfo

# Register your models here.

admin.site.register(ProductInfo,admin.ModelAdmin)
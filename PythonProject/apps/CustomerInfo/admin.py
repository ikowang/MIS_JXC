from django.contrib import admin
from apps.CustomerInfo.models import CustomerInfo

# Register your models here.

admin.site.register(CustomerInfo,admin.ModelAdmin)
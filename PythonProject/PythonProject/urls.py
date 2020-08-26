"""PythonProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.views.static import serve #需要导入
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),#这部分很重要
    url(r'^ProductClass/', include('apps.ProductClass.urls', namespace='ProductClass')),  # 商品类别模块
    url(r'^ProductInfo/', include('apps.ProductInfo.urls', namespace='ProductInfo')),  # 产品信息模块
    url(r'^Supplyer/', include('apps.Supplyer.urls', namespace='Supplyer')),  # 供应商模块
    url(r'^CustomerInfo/', include('apps.CustomerInfo.urls', namespace='CustomerInfo')),  # 客户信息模块
    url(r'^BuyInfo/', include('apps.BuyInfo.urls', namespace='BuyInfo')),  # 产品进货模块
    url(r'^SellInfo/', include('apps.SellInfo.urls', namespace='SellInfo')),  # 产品销售模块

    url(r'^', include("apps.Index.urls", namespace="Index")),  # 首页模块

    url(r'^tinymce/', include('tinymce.urls')),
]

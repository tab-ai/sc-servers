"""sc_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from farm_01.views import (Bt_dev_ViewSet, Bt_data_ViewSet, dashboard_api, catchall)


# django-rest-api Router
router = routers.DefaultRouter()
router.register('bt_dev', Bt_dev_ViewSet)
router.register('bt_data', Bt_data_ViewSet)

urlpatterns = [
    path('', catchall),
    path('admin/', admin.site.urls),
    path('api/', include('farm_01.urls')),
    path('api/', include(router.urls), name='api'), #REST API 페이지
]

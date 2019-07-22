"""pro_demo URL Configuration

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
from app_demo1 import views as demo1_v
from app_demo2 import views as demo2_v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index1/', demo1_v.index),
    path('index2/', demo2_v.index),
    path('test1/', demo1_v.test1),
    path('test_inapp/', demo1_v.test_inapp),
    path('area2d/', demo1_v.area2d),
    path('column3d/', demo1_v.column3d),
    path('ajax/', demo1_v.ajax),
    path('vue_elem/', demo1_v.vue_elem),
    path('get_all_user/', demo1_v.get_all_user),
    path('update_user/', demo1_v.update_user),
    path('get_reuqet_json/', demo1_v.get_reuqet_json),
]
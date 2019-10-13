"""zdjc URL Configuration

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
# from django.urls import path
from django.conf.urls import url as path

from app import views

urlpatterns = [
    path(r'^admin/', admin.site.urls),
    path(r"^$", views.index, name="index"),
    path("^send_email", views.send_email, name="send_email"),
    path('add_site/', views.add_site, name="add_site"),
    path('delete_site/', views.delete_site, name="delete_site"),
    path('verification/', views.verification, name="verification"),
    path('change_ignore/', views.change_ignore, name="change_ignore"),

    # 从tool.yuhuofei.it 获取站点数据并保持数据库中 
    # path('add_site_from_response/', views.set_data, name="set_data"),

    # 执行脚本
    path('run_script/', views.run_script, name="run_script"),
]

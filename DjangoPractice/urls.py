"""
URL configuration for DjangoPractice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from lab01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', views.main),
    path('person/', views.person),
    # 部门相关链接
    path('depart/list/', views.depart_list),
    path('depart/add/', views.depart_add),
    path('depart/delete/', views.depart_delete),
    path('depart/<int:nid>/edit/', views.depart_edit),

    # 员工相关链接
    path('user/list/', views.user_list),
    path('user/add/', views.user_add),
    path('user/modelform/add/', views.user_modelform_add),
    path('user/modelform/<int:nid>/edit/', views.user_modelform_edit),
    path('user/modelform/<int:nid>/delete/', views.user_modelform_delete),

    # 实验室相关
    path('lab/expe/list/', views.expe_list),
    path('lab/expe/record/', views.expe_record),
    path('lab/expe/add/', views.expe_add),
    path('lab/expe/<int:nid>/edit/', views.expe_edit),

    # 订单管理
    path('order/list/', views.order_list),

    # 文件管理
    path('upload/files/', views.upload_files),

    # 生成PDF文件
    # path("about/", views.some_view),

]

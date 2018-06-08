"""srs_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from srs_python import views as p_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^object/$',p_views.object),
    url(r'^srs/$',p_views.getData),
    url(r'^test/$',p_views.get_sys_info),
    url(r'^test2/$',p_views.get_sys_info2),
    url(r'^home/$',p_views.index,name='index'),
    url(r'^regist/$',p_views.regist,name='regist'),
    url(r'^login/$',p_views.log_in,name='login'),
    url(r'^logout/$',p_views.log_out,name='logout'),
    url(r'^create/$',p_views.create),
    url(r'^create_/$',p_views.create_),
    url(r'^files/$',p_views.files),
    url(r'^files/rename/$',p_views.file_rename),
    url(r'^files/del/$',p_views.file_del),
    url(r'^files/file_table_html/$',p_views.file_table_html),
    url(r'^files/upload_ajax/$',p_views.upload_ajax),
]

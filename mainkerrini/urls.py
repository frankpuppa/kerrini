from django.conf.urls import url
from mainkerrini import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^testvideo/$', views.testvideo, name='upload'),
]


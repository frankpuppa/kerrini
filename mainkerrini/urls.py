from django.conf.urls import include, url
from mainkerrini import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
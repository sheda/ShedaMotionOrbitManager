from django.conf.urls import url

from . import views

app_name = 'webcam'

urlpatterns = [
        url(r'^control$', views.control, name='control'),
        url(r'^$', views.index, name='index'),
]

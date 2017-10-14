from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^trips/$', views.trips, name='trips'),
    url(r'^update/$', views.update, name='update'),
]

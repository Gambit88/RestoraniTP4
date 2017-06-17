from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^guestRegister', views.registerGuests),
	url(r'^activate', views.activateGuest),
]

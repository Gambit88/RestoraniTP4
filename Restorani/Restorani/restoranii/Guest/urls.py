from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^guestRegister', views.registerGuests),
	url(r'^activate', views.activateGuest),
	url(r'^guestHomePage', views.guestPage, name = "guestHomePage"),
]
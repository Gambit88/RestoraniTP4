from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name="IndexPage"),
	url(r'^guestRegister', views.registerGuests),
	url(r'^activate', views.activateGuest),
	url(r'^login',views.loginRequest),
	url(r'^guestHomePage', views.guestPage, name = "guestHomePage"),
	url(r'^logout', views.logOut),
]

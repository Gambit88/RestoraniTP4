from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^guestRegister', views.registerGuests),
	url(r'^activate', views.activateGuest),
	url(r'^guestHomePage', views.guestPage, name = "guestHomePage"),
	url(r'^RestaurantList', views.restaurantList),
	url(r'^Friends', views.friends, name="friendsList"),
	url(r'^GuestProfile', views.profile, name="profileOfGuest"),
	url(r'^EditProfileGuest', views.editprofile),
	
]
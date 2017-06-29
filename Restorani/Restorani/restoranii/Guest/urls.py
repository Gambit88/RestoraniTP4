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
	url(r'^Reserve',views.res_part1),
	url(r'^tablePick',views.res_part2),
	url(r'^friendPick', views.res_part3),
	url(r'^fullReserve', views.res_part4),
	url(r'^confirmReservation', views.res_page),
	url(r'^aceptReservation', views.res_confirm),
	url(r'^declainReservation', views.res_deny),
	url(r'^rateRestaurant', views.rate),
	url(r'^orderFoodGuest', views.order_food),
	url(r'^cancelReservation', views.cancel_res),
]
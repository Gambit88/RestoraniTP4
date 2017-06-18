from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name="IndexPage"),
	url(r'^guestRegister', views.registerGuests),
	url(r'^activate', views.activateGuest),
	url(r'^login',views.loginRequest),
	url(r'^guestHomePage', views.guestPage, name = "guestHomePage"),
	url(r'^logout', views.logOut, name="logOut"),
	url(r'^restaurantReg', views.registarRestaurant),
	url(r'restaurantManReg', views.registarRestaurantMan),
	url(r'employeeReg', views.registarEmployee),
	url(r'^cookHomePage', views.cookPage, name = "cookHomePage"),
	url(r'^bartenderHomePage', views.bartenderPage, name = "bartenderHomePage"),
	url(r'^waiterHomePage', views.waiterPage, name = "waiterHomePage"),
	url(r'^changePassword', views.firstLogin),
]

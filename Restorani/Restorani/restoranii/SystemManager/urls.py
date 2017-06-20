from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^restaurantReg', views.registarRestaurant),
	url(r'^restaurantManReg', views.registarRestaurantMan),
	url(r'^smHomePage',views.SystemManPage, name = 'SMHomePage'),
	url(r'^SystemManagerReg', views.registarSystemMan),
]
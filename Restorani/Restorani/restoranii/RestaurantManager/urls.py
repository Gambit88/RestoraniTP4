from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^employeeReg', views.registarEmployee),
	url(r'^rmHomePage',views.restaurantManagerHome, name = 'RMHomePage'),
	url(r'^beverages', views.drinks),
	url(r'^meal', views.food),
	url(r'^supplier', views.supplier),
	url(r'^updateRestaurant', views.updateRest),
]
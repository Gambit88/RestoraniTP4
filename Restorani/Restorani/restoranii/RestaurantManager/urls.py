from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^employeeReg', views.registarEmployee),
	url(r'^rmHomePage',views.restaurantManagerHome, name = 'RMHomePage'),
	url(r'^beverages', views.drinks),
	url(r'^meal', views.food),
	url(r'^supplier', views.supplier),
	url(r'^updateRestaurant', views.updateRest),
	url(r'^segments', views.addSegment),
	url(r'^tables', views.tableLayout),
	url(r'^order', views.managerOrder),
	url(r'^schedule', views.schedule),
	url(r'^viewOffers', views.viewOffers),
]
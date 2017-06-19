from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^employeeReg', views.registarEmployee),
	url(r'^rmHomePage',views.restaurantManagerHome, name = 'RMHomePage')
]
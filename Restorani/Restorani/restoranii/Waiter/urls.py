from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^waiterHomePage', views.waiterPage, name = "waiterHomePage"),
	url(r'^waiterProfile', views.waiterProfile, name = "waiterProfile"),
	url(r'^editWaiterProfile', views.editWaiterProfile, name = "editWaiterProfile"),
	url(r'^editWaiterPassword', views.changeWaiterPassword, name = "editWaiterPassword"),
]
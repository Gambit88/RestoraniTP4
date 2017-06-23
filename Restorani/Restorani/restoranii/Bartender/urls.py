from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^bartenderHomePage', views.bartenderPage, name = "bartenderHomePage"),
	url(r'^bartenderProfile', views.bartenderProfile, name = "bartenderProfile"),
	url(r'^editBartenderProfile', views.editBartenderProfile, name = "editBartenderProfile"),
	url(r'^editBartenderPassword', views.changeBartenderPassword, name = "editBartenderPassword"),
]
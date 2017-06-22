from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^cookHomePage', views.cookPage, name = "cookHomePage"),
	url(r'^cookProfile', views.cookProfile, name = "cookProfile"),
	url(r'^editCookProfile', views.editCookProfile, name = "editCookProfile"),
	url(r'^editCookPassword', views.changePassword, name = "editCookPassword"),
]
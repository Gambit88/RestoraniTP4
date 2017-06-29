from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^waiterHomePage', views.waiterPage, name = "waiterHomePage"),
	url(r'^waiterProfile', views.waiterProfile, name = "waiterProfile"),
	url(r'^editWaiterProfile', views.editWaiterProfile, name = "editWaiterProfile"),
	url(r'^editWaiterPassword', views.changeWaiterPassword, name = "editWaiterPassword"),
	url(r'^addOrder', views.addOrder),
	url(r'^saveOrder', views.saveOrder, name = "saveOrder"),
	url(r'^editOrder', views.editOrder, name = "editOrder"),
	url(r'^createBill', views.createBill, name="createBill"),
	url(r'^payOrder', views.payOrder, name="payOrder"),
	url(r'^addFood', views.addFood, name = "addFood"),
	url(r'^addDrink', views.addDrink, name = "addDrink"),
	url(r'^saveFoods', views.saveFoods, name = "saveFoods"),
	url(r'^saveDrinks', views.saveDrinks, name = "saveDrinks"),
	url(r'^removeFood', views.removeFood, name = "removeFood"),
	url(r'^removeDrink', views.removeDrink, name = "removeDrink"),
]
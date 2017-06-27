from django.conf.urls import include, url
from . import views
from django.contrib import admin

urlpatterns = [
    url(r'^sHomePage', views.supplierHome, name='supplierHomePage'),
    url(r'^allPosts', views.allPosts),
    url(r'^myOffers', views.myOffers),
    url(r'^updateOffer', views.updateOffer),
]
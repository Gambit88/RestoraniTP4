from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name="IndexPage"),
	url(r'^login',views.loginRequest),
	url(r'^logout', views.logOut, name="logOut"),
	url(r'^changePassword', views.firstLogin),
	url(r'^admin',views.sysAdmin),
	url(r'^recheckReservations',views.recheck),
]

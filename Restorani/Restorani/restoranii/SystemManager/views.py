from django.shortcuts import render
from django.template import loader
from restorani.models import SystemManager
from restorani.models import Restaurant
from restorani.models import RestaurantManager
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test,login_required
from django.views.decorators.csrf import csrf_exempt
from geopy.geocoders import Nominatim
# Create your views here.

#uslov za pristump stranici kao menadzer sistema
def SystemManCheck(systemManager):
	return systemManager.first_name=="SYSTEM"
#home stranica za menagera sistema
@user_passes_test(SystemManCheck,login_url='./')
def SystemManPage(request):
	template = loader.get_template("SMHomePage.html")
	system = SystemManager.objects.get(email = request.user.username)
	return HttpResponse(template.render({'system': system}))

#registracija novog restorana
@csrf_exempt
@user_passes_test(SystemManCheck,login_url='./')
def registarRestaurant(request):
	list = Restaurant.objects.all()
	if request.method == 'POST':
		if not request.POST.get('name'):
			error = 'Name has not been submited'
			link = "./restaurantReg"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not  request.POST.get('type'):
			error = 'Type has not been submited'
			link = "./restaurantReg"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not  request.POST.get('address'):
			error = 'Address has not been submited'
			link = "./restaurantReg"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not  request.POST.get('dimX') or not request.POST.get('dimY'):
			error = 'Dimension has not been submited'
			link = "./restaurantReg"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		geolocator = Nominatim()
		try:
			location = geolocator.geocode(request.POST.get('address'))
		except:
			error = 'Address could not be located at this time.'
			link = "./restaurantReg"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if location is None:
			error = 'Address could not be located, try using your countrys language.'
			link = "./restaurantReg"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		restaurant = Restaurant.objects.create(name = request.POST.get('name'), type = request.POST.get('type'), address =request.POST.get('address') , sizeX = request.POST.get('dimX'), sizeY = request.POST.get('dimY'), long=location.longitude, lat=location.latitude)
	template = loader.get_template("restaurantReg.html")
	return HttpResponse(template.render({'lista': list}))

#registracija menadzera restorana
@csrf_exempt
@user_passes_test(SystemManCheck,login_url='./')
def registarRestaurantMan(request):
	list = Restaurant.objects.all()
	managers = RestaurantManager.objects.all()
	if request.method == 'POST':
		restaurantID = Restaurant.objects.get(name = request.POST.get('r'))
		if not request.POST.get('name'):
			error = 'Name has not been submited'
			link = "./restaurantManReg"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not  request.POST.get('lastname'):
			error = 'Last Name has not been submited'
			link = "./restaurantManReg"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not  request.POST.get('email'):
			error = 'Email has not been submited'
			link = "./restaurantManReg"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		user = User.objects.create_user(username = request.POST.get('email'), first_name = "MANAGER", password = "manager")
		restaurantManager = RestaurantManager.objects.create(name = request.POST.get('name'), surname = request.POST.get('lastname'), email = request.POST.get('email') , restaurant = restaurantID, user = user)
	template = loader.get_template("restaurantManReg.html")
	return HttpResponse(template.render({'lista': list, 'managers': managers}))

#registracija menadzera sistema
@csrf_exempt
@user_passes_test(SystemManCheck,login_url='./')
def registarSystemMan(request):
	sysManager = SystemManager.objects.all()
	if request.method == 'POST':
		if not request.POST.get('name'):
			error = 'Name has not been submited'
			link = "SystemManagerReg"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not request.POST.get('lastname'):
			error = 'Last Name has not been submited'
			link = "SystemManagerReg"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not request.POST.get('email'):
			error = 'Email has not been submited'
			link = "SystemManagerReg"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		user = User.objects.create_user(username = request.POST.get('email'), first_name = "SYSTEM", password = "admin")
		system = SystemManager.objects.create(name = request.POST.get('name'), surname = request.POST.get('lastname'), email = request.POST.get('email'), user = user)
	template = loader.get_template("SystemManagerReg.html")
	return HttpResponse(template.render({'sysManager': sysManager}))
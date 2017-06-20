from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from restorani.models import Employee
from restorani.models import Cook
from restorani.models import Waiter
from restorani.models import Bartender
from restorani.models import Restaurant
from restorani.models import RestaurantManager
from restorani.models import Beaverage
from restorani.models import Food
from restorani.models import Supplier
from restorani.models import Employee
from django.contrib.auth.decorators import user_passes_test,login_required
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

#uslov za pristump stranici kao menadzer restorana
def restaurantManagerCheck(restaurantManager):
	return restaurantManager.first_name=="MANAGER"

#home stranica za menagera sistema
@user_passes_test(restaurantManagerCheck,login_url='./')
def restaurantManagerHome(request):
	template = loader.get_template("RMHomePage.html")
	manager = RestaurantManager.objects.get(email = request.user.username)
	return HttpResponse(template.render({'manager': manager}))

#registracija zaposlenih
@csrf_exempt
@user_passes_test(restaurantManagerCheck,login_url='./')
def registarEmployee(request):
	manager = RestaurantManager.objects.get(email = request.user.username)
	restaurantID = Restaurant.objects.get(name = manager.restaurant.name)
	print(restaurantID.name)
	employees = Employee.objects.filter(restaurant = restaurantID.pk)
	if request.method == 'POST':
		if not request.POST.get('name'):
			error = 'Name has not been submited'
			link = "./employeeReg"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not request.POST.get('lastname'):
			error = 'Last Name has not been submited'
			link = "./employeeReg"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not request.POST.get('email'):
			error = 'Email has not been submited'
			link = "./employeeReg"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not request.POST.get('shoe'):
			error = 'Shoe size has not been submited'
			link = "./employeeReg"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if request.POST.get('job') == "Cook":
			if not request.POST.get('type'):
				error = 'Type of cook has not been submited'
				link = "./employeeReg"
				template = loader.get_template("error.html")
				return HttpResponse(template.render({'error': error, 'link': link}))
		if request.POST.get('job') == "Waiter":
			user = User.objects.create_user(username = request.POST.get('email'), first_name = "WAITER", password = "waiter", last_name = True)
			waiter = Waiter.objects.create(name=request.POST.get('name'),
												 surname=request.POST.get('lastname'), email=request.POST.get('email'),
												 shoeSize=request.POST.get('shoe'), size=request.POST.get('size'),
												 user=user,
												 restaurant=restaurantID, firstLogin = False)
		if request.POST.get('job') == "Bartender":
			user = User.objects.create_user(username = request.POST.get('email'), first_name = "BARTENDER", password = "bartender", last_name = True)
			bartender = Bartender.objects.create(name=request.POST.get('name'),
									   surname=request.POST.get('lastname'), email=request.POST.get('email'),
									   shoeSize=request.POST.get('shoe'), size=request.POST.get('size'), user=user,
									   restaurant=restaurantID, firstLogin = False)

		if request.POST.get('job') == "Cook":
			user = User.objects.create_user(username=request.POST.get('email'), first_name="COOK", password="cook", last_name = True)
			cook = Cook.objects.create(kind=request.POST.get('type'), name = request.POST.get('name'), surname = request.POST.get('lastname'), email = request.POST.get('email'),
										   shoeSize = request.POST.get('shoe'), size = request.POST.get('size'), user = user, restaurant = restaurantID, firstLogin = False)

	template = loader.get_template("employeeReg.html")
	return HttpResponse(template.render({'rest': manager.restaurant.name, 'employee': employees}))

#dodavanje pica za odredjeni restoran
@csrf_exempt
@user_passes_test(restaurantManagerCheck,login_url='./')
def drinks(request):
	manager = RestaurantManager.objects.get(email = request.user.username)
	restaurant = Restaurant.objects.get(pk=manager.restaurant_id)
	getDrinks = Beaverage.objects.filter(restaurant = restaurant.pk)
	if request.method == "POST":
		if not request.POST.get('name'):
			error = 'Name has not been submited'
			link = "beverages.html"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not request.POST.get('description'):
			error = 'Description has not been submited'
			link = "beverages.html"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not request.POST.get('price'):
			error = 'Price has not been submited'
			link = "beverages.html"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))

		beverage = Beaverage.objects.create(name = request.POST.get('name'), description = request.POST.get('description'), price = request.POST.get('price'), restaurant = restaurant)
	template = loader.get_template("beverages.html")
	return HttpResponse(template.render({'rest': restaurant,'drinks': getDrinks}))

#dodavanje jela za odredjeni restoran
@csrf_exempt
@user_passes_test(restaurantManagerCheck,login_url='./')
def food(request):
	manager = RestaurantManager.objects.get(email = request.user.username)
	restaurant = Restaurant.objects.get(pk=manager.restaurant_id)
	getfood = Food.objects.filter(restaurant = restaurant.pk)
	if request.method == "POST":
		if not request.POST.get('name'):
			error = 'Name has not been submited'
			link = "meal.html"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not request.POST.get('description'):
			error = 'Description has not been submited'
			link = "meal.html"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not request.POST.get('price'):
			error = 'Price has not been submited'
			link = "meal.html"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))

		food = Food.objects.create(name = request.POST.get('name'), description = request.POST.get('description'), price = request.POST.get('price'), restaurant = restaurant)
	template = loader.get_template("meal.html")
	return HttpResponse(template.render({'rest': restaurant,'food': getfood}))

#registracija ponudjaca
@csrf_exempt
@user_passes_test(restaurantManagerCheck,login_url='./')
def supplier(request):
	manager = RestaurantManager.objects.get(email = request.user.username)
	restaurant = Restaurant.objects.get(pk = manager.restaurant_id)
	getSuppliers = Supplier.objects.all()
	if request.method == "POST":
		if not request.POST.get('name'):
			error = 'Name has not been submited'
			link = "supplier.html"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not request.POST.get('lastname'):
			error = 'Last Name has not been submited'
			link = "supplier.html"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not request.POST.get('email'):
			error = 'Email has not been submited'
			link = "supplier.html"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		user = User.objects.create_user(username = request.POST.get('email'), first_name = "SUPPLIER",
										password = "supplier", last_name = True)
		supplier = Supplier.objects.create(name = request.POST.get('name'), surname = request.POST.get('lastname'), email = request.POST.get('email'), user = user)
	template = loader.get_template("supplier.html")
	return HttpResponse(template.render({'rest': restaurant,'supplier': getSuppliers}))

#izmena restorana
@csrf_exempt
@user_passes_test(restaurantManagerCheck,login_url='./')
def updateRest(request):
	manager = RestaurantManager.objects.get(email = request.user.username)
	restaurant = Restaurant.objects.get(pk = manager.restaurant_id)
	if request.method == "POST":
		if not request.POST.get('name') or not request.POST.get('type'):
			error = "You didn't input any changes"
			link = "updateRestaurant.html"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if request.POST.get('name'):
			name = request.POST.get('name')
			restaurant.name = name
		if request.POST.get('type'):
			type = request.POST.get('type')
			restaurant.type = type
		restaurant.save()
	template = loader.get_template("updateRestaurant.html")
	return HttpResponse(template.render({'rest': restaurant}))
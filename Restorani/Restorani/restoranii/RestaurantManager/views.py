from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import template
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
from restorani.models import Segment
from restorani.models import RestaurantTable
from restorani.models import Post
from restorani.models import TableHelp
from datetime import datetime
from django.template.defaulttags import register
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
		if not request.POST.get('name') and not request.POST.get('type'):
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

@csrf_exempt
@user_passes_test(restaurantManagerCheck,login_url='./')
def addSegment(request):
	manager = RestaurantManager.objects.get(email = request.user.username)
	restaurant = Restaurant.objects.get(pk = manager.restaurant_id)
	if request.method == "GET":
		try:
			allSegments = Segment.objects.filter(restaurant = restaurant.pk)
			template = loader.get_template("segments.html")
			return HttpResponse(template.render({'rest': restaurant, 'segments': allSegments}))
		except:
			template = loader.get_template("segments.html")
			return HttpResponse(template.render({'rest': restaurant}))
	if request.method == "POST":
		if not request.POST.get('name'):
			error = "You didn't input segment"
			link = "segments.html"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		segment = Segment.objects.create(name=request.POST.get('name'), restaurant=restaurant)
		allSegments = Segment.objects.filter(restaurant = restaurant.pk)
		template = loader.get_template("segments.html")
		return HttpResponse(template.render({'rest': restaurant, 'segments': allSegments}))


@csrf_exempt
@user_passes_test(restaurantManagerCheck,login_url='./')
def tableLayout(request):
	manager = RestaurantManager.objects.get(email = request.user.username)
	restaurant = Restaurant.objects.get(pk = manager.restaurant_id)
	allSegments = Segment.objects.filter(restaurant=restaurant.pk)
	tables = RestaurantTable.objects.filter(restaurant = restaurant)
	tableX = []
	tableY = []
	for t in tables:
		tableX.append(t.posX)
		tableY.append(t.posY)
	tlist = []
	for i in range(restaurant.sizeX):
		for j in range(restaurant.sizeY):
			test = True
			for table in tables:
				if i == table.posX and j == table.posY:
					# ubaci proveru da li je rezervisan za kasnije, pa ako jeste nemoj da dozvolis da se menja/brise? promenis True na False za status?
					tableH = TableHelp()
					tableH.posX = i
					tableH.posY = j
					tableH.status = True
					tableH.num = table.tableNo
					tableH.segment = table.segment.name
					tableH.id = table.id
					tlist.append(tableH)
					test = False
			if test:
				tableH = TableHelp()
				tableH.posX = i
				tableH.posY = j
				tableH.status = False
				tableH.num = ""
				tableH.segment = ""
				tableH.id = -1
				tlist.append(tableH)
	if request.method == "GET":
		try:
			template = loader.get_template("tables.html")
			return HttpResponse(template.render({'rest': restaurant, 'segments': allSegments, 'rangeX': range(restaurant.sizeX),
												 'rangeY': range(restaurant.sizeY), 'tlist': tlist}))
		except:
			template = loader.get_template("tables.html")
			return HttpResponse(template.render({'rest': restaurant}))
	if request.method == "POST":
		segment = Segment.objects.get(name = request.POST.get('r'), restaurant = restaurant)
		table = RestaurantTable.objects.create(tableNo = request.POST.get('table'), segment = segment, chairNo = request.POST.get('chair'),
											   posX = request.POST.get('x'), posY = request.POST.get('y'), restaurant = restaurant)
		template = loader.get_template("tables.html")
		return HttpResponse(template.render(
			{'rest': restaurant, 'segments': allSegments, 'rangeX': range(restaurant.sizeX),
			 'rangeY': range(restaurant.sizeY), 'tlist': tlist}))

@csrf_exempt
@user_passes_test(restaurantManagerCheck,login_url='./')
def managerOrder(request):
	manager = RestaurantManager.objects.get(email=request.user.username)
	restaurant = Restaurant.objects.get(pk=manager.restaurant_id)
	if request.method == "GET":
		try:
			allPosts = Post.objects.all()
			template = loader.get_template("orderFromManager.html")
			return HttpResponse(template.render({'rest': restaurant, 'posts': allPosts}))
		except:
			template = loader.get_template("orderFromManager.html")
			return HttpResponse(template.render({'rest': restaurant}))
	if request.method == "POST":
		if not request.POST.get('name'):
			error = "You didn't input order"
			link = "orderFromManager.html"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		if not request.POST.get('date'):
			error = "You didn't input date"
			link = "orderFromManager.html"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		try:
			valid_datetime = datetime.strptime(request.POST.get('date'), '%Y-%m-%d %H:%M')
		except:
			error = "Invalid date"
			link = "orderFromManager.html"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		print(request.POST.get('date'))
		post = Post.objects.create(content = request.POST.get('name'), expiration_date = valid_datetime, restaurant = restaurant)
		allPosts = Post.objects.all()
		template = loader.get_template("orderFromManager.html")
		return HttpResponse(template.render({'rest': restaurant, 'posts': allPosts}))
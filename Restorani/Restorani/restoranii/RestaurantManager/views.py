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
from restorani.models import Schedule
from restorani.models import Offer
from restorani.models import Reservation
from restorani.models import RatingRestaurant
from restorani.models import RatingServices
from restorani.models import RatingFood
from restorani.models import Order
import datetime
from django.core.mail import send_mail
from django.template.defaulttags import register
from django.contrib.auth.decorators import user_passes_test,login_required
from django.views.decorators.csrf import csrf_exempt
import smtplib
import _thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.db import connection
# Create your views here.

#uslov za pristump stranici kao menadzer restorana
def restaurantManagerCheck(restaurantManager):
	return restaurantManager.first_name=="MANAGER"

#home stranica za menagera sistema
@login_required(redirect_field_name='IndexPage')
@user_passes_test(restaurantManagerCheck,login_url='./')
def restaurantManagerHome(request):
	template = loader.get_template("RMHomePage.html")
	manager = RestaurantManager.objects.get(email = request.user.username)
	return HttpResponse(template.render({'manager': manager}))

#registracija zaposlenih
@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(restaurantManagerCheck,login_url='./')
def registarEmployee(request):
	manager = RestaurantManager.objects.get(email = request.user.username)
	restaurantID = Restaurant.objects.get(name = manager.restaurant.name)
	print(restaurantID.name)
	employees = Employee.objects.filter(restaurant = restaurantID.pk)
	if request.method == 'POST':
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
@login_required(redirect_field_name='IndexPage')
@user_passes_test(restaurantManagerCheck,login_url='./')
def drinks(request):
	manager = RestaurantManager.objects.get(email = request.user.username)
	restaurant = Restaurant.objects.get(pk=manager.restaurant_id)
	getDrinks = Beaverage.objects.filter(restaurant = restaurant.pk)
	if request.method == "POST":
		beverage = Beaverage.objects.create(name = request.POST.get('name'), description = request.POST.get('description'), price = request.POST.get('price'), restaurant = restaurant)
	template = loader.get_template("beverages.html")
	return HttpResponse(template.render({'rest': restaurant,'drinks': getDrinks}))

#dodavanje jela za odredjeni restoran
@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(restaurantManagerCheck,login_url='./')
def food(request):
	manager = RestaurantManager.objects.get(email = request.user.username)
	restaurant = Restaurant.objects.get(pk=manager.restaurant_id)
	getfood = Food.objects.filter(restaurant = restaurant.pk)
	if request.method == "POST":
		food = Food.objects.create(name = request.POST.get('name'), description = request.POST.get('description'), price = request.POST.get('price'), restaurant = restaurant)
	template = loader.get_template("meal.html")
	return HttpResponse(template.render({'rest': restaurant,'food': getfood}))

#registracija ponudjaca
@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(restaurantManagerCheck,login_url='./')
def supplier(request):
	manager = RestaurantManager.objects.get(email = request.user.username)
	restaurant = Restaurant.objects.get(pk = manager.restaurant_id)
	getSuppliers = Supplier.objects.all()
	if request.method == "POST":
		user = User.objects.create_user(username = request.POST.get('email'), first_name = "SUPPLIER",
										password = "supplier", last_name = True)
		supplier = Supplier.objects.create(name = request.POST.get('name'), surname = request.POST.get('lastname'), email = request.POST.get('email'), user = user)
	template = loader.get_template("supplier.html")
	return HttpResponse(template.render({'rest': restaurant,'supplier': getSuppliers}))

#izmena restorana
@csrf_exempt
@login_required(redirect_field_name='IndexPage')
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
@login_required(redirect_field_name='IndexPage')
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
		segment = Segment.objects.create(name=request.POST.get('name'), restaurant=restaurant)
		allSegments = Segment.objects.filter(restaurant = restaurant.pk)
		template = loader.get_template("segments.html")
		return HttpResponse(template.render({'rest': restaurant, 'segments': allSegments}))


@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(restaurantManagerCheck,login_url='./')
def tableLayout(request):
	id = None
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
		if request.POST.get('type') == "add":
			segment = Segment.objects.get(name = request.POST.get('r'), restaurant = restaurant)
			table = RestaurantTable.objects.create(tableNo = request.POST.get('table'), segment = segment, chairNo = request.POST.get('chair'),
											   posX = request.POST.get('x'), posY = request.POST.get('y'), restaurant = restaurant)

		if request.POST.get('type') == "remove":
			try:
				x = RestaurantTable.objects.get(tableNo = request.POST.get('delete'), restaurant = restaurant)
				try:
					res = Reservation.objects.get(restaurantTables = x)
					error = "Cant't change this table it's reserved"
					link = "tables.html"
					template = loader.get_template("error.html")
					return HttpResponse(template.render({'error': error, 'link': link}))
				except:
					y = RestaurantTable.objects.get(pk = x.pk).delete()
			except:
				error = "Table doesn't exist"
				link = "tables.html"
				template = loader.get_template("error.html")
				return HttpResponse(template.render({'error': error, 'link': link}))

		if request.POST.get('type') == "change":
			if not request.POST.get('tno'):
				error = "Table doesn't exist"
				link = "tables.html"
				template = loader.get_template("error.html")
				return HttpResponse(template.render({'error': error, 'link': link}))
			try:
				id = RestaurantTable.objects.get(tableNo = request.POST.get('tno'), restaurant = restaurant)
				try:
					res = Reservation.objects.get(restaurantTables = id)
					print(res)
					print("---------------------------------")
					error = "Cant't change this table it's reserved"
					link = "tables.html"
					template = loader.get_template("error.html")
					return HttpResponse(template.render({'error': error, 'link': link}))
				except:
					pass
			except:
				error = "Table doesn't exist"
				link = "tables.html"
				template = loader.get_template("error.html")
				return HttpResponse(template.render({'error': error, 'link': link}))

		if request.POST.get('type') == "final":
			change = RestaurantTable.objects.get(pk = request.POST.get('id'))
			change.segment = Segment.objects.get(name = request.POST.get('newseg'), restaurant = restaurant)
			change.chairNo = request.POST.get('newchair')
			change.save()

		tables = RestaurantTable.objects.filter(restaurant=restaurant)
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
		template = loader.get_template("tables.html")
		return HttpResponse(template.render(
			{'rest': restaurant, 'segments': allSegments, 'rangeX': range(restaurant.sizeX),
			 'rangeY': range(restaurant.sizeY), 'tlist': tlist, 'id': id}))

@csrf_exempt
@login_required(redirect_field_name='IndexPage')
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
			valid_datetime = request.POST.get('date').split('T')[0] + ' ' + request.POST.get('date').split('T')[1]
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

@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(restaurantManagerCheck,login_url='./')
def schedule(request):
	manager = RestaurantManager.objects.get(email = request.user.username)
	restaurant = Restaurant.objects.get(pk = manager.restaurant_id)
	employees = Employee.objects.filter(restaurant = restaurant)
	segment = Segment.objects.filter(restaurant = restaurant)
	shift = Schedule.objects.all()
	if request.method == "POST":
		employee = Employee.objects.get(pk = request.POST.get('r'))
		type = employee.user.first_name
		date1 = request.POST.get('date').split('T')[0]
		section = None
		if type == "WAITER":
			section = Segment.objects.get(pk = request.POST.get('section'), restaurant=restaurant)
			schedule = Schedule.objects.create(segment=section, employee=employee, shift=request.POST.get('shift'),
											   date=date1)
		else:
			schedule = Schedule.objects.create(segment = section, employee = employee, shift = request.POST.get('shift'), date = date1)
	s = Schedule.objects.all()
	sc = []
	for i in s:
		if i.employee.restaurant == restaurant:
			sc.append(i)
	shift1 = []
	shift2 = []
	shift3 = []
	for i in sc:
		if i.shift == 1:
			shift1.append(i)
		if i.shift == 2:
			shift2.append(i)
		if i.shift == 3:
			shift3.append(i)
	today = datetime.date.today()
	calendar1 = []
	calendar1.append(today)
	for i in range(1, 5):
		today = today + datetime.timedelta(days=1)
		calendar1.append(today)
	calendar = []
	for i in calendar1:
		g = str(i)
		calendar.append(g)
	for i in shift1:
		i.date = str(i.date).split(' ')[0]
		i.save()
	for i in shift2:
		i.date = str(i.date).split(' ')[0]
		i.save()
	for i in shift3:
		i.date = str(i.date).split(' ')[0]
		i.save()

	template = loader.get_template("schedule.html")
	return HttpResponse(template.render({'employees': employees, 'segment': segment, 'rest': restaurant, 'x': shift, 'calendar':calendar,'shift1': shift1,'shift2': shift2,'shift3': shift3}))

@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(restaurantManagerCheck,login_url='./')
def viewOffers(request):
	manager = RestaurantManager.objects.get(email=request.user.username)
	restaurant = Restaurant.objects.get(pk=manager.restaurant_id)
	if request.method == "GET":
		try:
			offers = Offer.objects.all()
			offerList = []
			for o in offers:
				if o.post.restaurant == restaurant:
					offerList.append(o)
			temp = []
			for i in offerList:
				if i.acepted == True:
					temp.append(i)
			if temp:
				for i in temp:
					for j in offerList:
						if i.post == j.post:
							offerList.remove(j)
			for i in offerList:
				if i.acepted == True:
					offerList.remove(i)
			template = loader.get_template("viewOffers.html")
			return HttpResponse(template.render({'offers': offerList}))
		except:
			error = "No offers"
			link = "rmHomePage.html"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
	if request.method == "POST":
		lista = request.POST.get('lista')
		list = lista[:-1]

		cursor = connection.cursor()
		cursor.execute("LOCK TABLES restorani_offer WRITE, restorani_post WRITE, restorani_restaurant WRITE, restorani_supplier WRITE")
		offers = Offer.objects.all()
		offerList = []
		temp = []
		tem2 = []
		for o in offers:
			if o.post.restaurant == restaurant:
				offerList.append(o)
		for i in offerList:
			if i.acepted == True:
				temp.append(i)
				tem2.append(i)
		if temp:
			for i in temp:
				for j in offerList:
					if i.post == j.post:
						offerList.remove(j)
						tem2.append(j)
		for i in offerList:
			if i.acepted == True:
				offerList.remove(i)

		x = 0
		for i in list.split(" "):
			x += 1
		if len(offerList) != x:
			cursor.execute("UNLOCK TABLES;")
			err = "New offer has arrived-------duzine nisu jednae!!!"
			link = "viewOffers.html"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': err, 'link': link}))
		else:
			part = list.split(" ")
			for i in part:
				parts = i.split(",")
				id = int(parts[0])
				price = parts[1]
				for j in offerList:
					if id == j.pk:
						if price != j.price:
							cursor.execute("UNLOCK TABLES;")
							err = "New offer has arrived--razlicite cene!!!"
							link = "viewOffers.html"
							template = loader.get_template("error.html")
							return HttpResponse(template.render({'error': err, 'link': link}))
						else:
							print("jednaki")

		offer = Offer.objects.get(pk = request.POST.get('hidden'))
		offer = Offer.objects.get(pk = request.POST.get('hidden'))
		offer.acepted = True
		offer.save()
		offers = Offer.objects.all()
		offerList = []
		temp = []
		tem2 = []
		for o in offers:
			if o.post.restaurant == restaurant:
				offerList.append(o)
		for i in offerList:
			if i.acepted == True:
				temp.append(i)
				tem2.append(i)
		if temp:
			for i in temp:
				for j in offerList:
					if i.post == j.post:
						offerList.remove(j)
						tem2.append(j)
		for i in offerList:
			if i.acepted == True:
				offerList.remove(i)
		for i in tem2:
			_thread.start_new_thread(sendEmail, (i.supplier.email,offer))
		template = loader.get_template("viewOffers.html")
		return HttpResponse(template.render({'offers': offerList}))


def sendEmail(email, offer):
	fromaddr = "tp4restoranii@gmail.com"
	toaddr = email
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Answer to your offer"
	if email == offer.supplier.email:
		body = "<html><head></head><body>'It is our pleasure to let you know that your offer is accepted</body></html>"
	else:
		body = "<html><head></head><body>'We are sorry to tell you that your offer wasn't accepted</body></html>"
	msg.attach(MIMEText(body, 'html'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "restorani")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(restaurantManagerCheck,login_url='./')
def avgerage(request):
	manager = RestaurantManager.objects.get(email=request.user.username)
	restaurant = Restaurant.objects.get(pk=manager.restaurant_id)
	ratings = RatingRestaurant.objects.filter(restaurant=restaurant)
	waiters = Waiter.objects.filter(restaurant = restaurant)
	foods = Food.objects.filter(restaurant = restaurant)
	avrRate = 0
	numr = 0
	counter = 0
	total = 0
	counterf = 0
	totalf = 0
	for rating in ratings:
		avrRate = avrRate + rating.rating
		numr = numr + 1
	if numr != 0:
		avrRate = avrRate / numr
	if request.method == "POST":
		if request.POST.get('type') == "w":
			waiter = Waiter.objects.get(pk = request.POST.get('r'))
			r = RatingServices.objects.filter(employee = waiter)
			for i in r:
				total += i.rating
				counter += 1
			try:
				total = total / counter
			except:
				error = "No ratings for waiter"
				link = "average.html"
				template = loader.get_template("error.html")
				return HttpResponse(template.render({'error': error, 'link': link}))
		if request.POST.get('type') == "f":
			food = Food.objects.filter(pk = request.POST.get('f'))
			r = RatingFood.objects.filter(food = food)
			for i in r:
				totalf += i.rating
				counterf += 1
			try:
				totalf = totalf / counterf
			except:
				error = "No ratings for food"
				link = "average.html"
				template = loader.get_template("error.html")
				return HttpResponse(template.render({'error': error, 'link': link}))
	template = loader.get_template("average.html")
	return HttpResponse(template.render({'avg': avrRate, 'waiters': waiters, 'totalW': total, 'totalf': totalf, 'food': foods}))

@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(restaurantManagerCheck,login_url='./')
def waiterProfit(request):
	manager = RestaurantManager.objects.get(email=request.user.username)
	restaurant = Restaurant.objects.get(pk=manager.restaurant_id)
	waiters = Waiter.objects.filter(restaurant=restaurant)
	total = ""
	if request.method == "POST":
		waiter = Waiter.objects.get(pk=request.POST.get('r'))
		orders = Order.objects.filter(employees=waiter)
		totalFood = 0
		totalDrinks = 0
		for i in orders:
			for j in i.orderedfoods.all():
				totalFood = j.food.price * j.amount
			for j in i.ordereddrinks.all():
				totalDrinks = j.beaverage.price * j.amount
		total = totalFood + totalDrinks
	template = loader.get_template("waiterProfit.html")
	return HttpResponse(template.render({'waiters': waiters, 'total': total}))

@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(restaurantManagerCheck,login_url='./')
def restProfit(request):
	manager = RestaurantManager.objects.get(email=request.user.username)
	restaurant = Restaurant.objects.get(pk=manager.restaurant_id)
	o = Order.objects.all()
	orders = []
	total = ""
	for i in o:
		for j in i.employees.all():
			if j.restaurant == restaurant:
				if i not in orders:
					orders.append(i)
	totalFood = 0
	totalDrinks = 0
	for i in orders:
		for j in i.orderedfoods.all():
			totalFood = j.food.price * j.amount
		for j in i.ordereddrinks.all():
			totalDrinks = j.beaverage.price * j.amount
	total = totalFood + totalDrinks
	template = loader.get_template("restaurantProfit.html")
	return HttpResponse(template.render({'profit': total}))
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from restorani.models import Guest
from restorani.models import Reservation
from restorani.models import Restaurant
from restorani.models import RestaurantTable, Food, Beaverage, Waiter, Order, OrderedFood, OrderedDrink
from django.contrib.auth.models import User
import smtplib
import _thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.decorators import user_passes_test,login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.db.models import Q
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from django.template.defaulttags import register
from restorani.models import RatingRestaurant, InviteList
from validate_email import validate_email
from restorani.models import TableHelp
from datetime import datetime, timedelta
from django.db import connection
from django.utils import timezone
from restorani.models import RatingFood,RatingRestaurant,RatingServices, Schedule

# Create your views here.
#registracija
@csrf_exempt
def registerGuests(request):
	if request.method == 'GET':
		template = loader.get_template("static/guestRegister.html")
		return HttpResponse(template.render())
	if request.method == 'POST':
		email = request.POST.get('email')
		#PROVERE ISPRAVNOSTI UNOSA
		if not email:
			err = "Email address has not been submited."
			link = "./guestRegister"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error':err , 'link':link}))
		if not request.POST.get('password'):
			err = "Password has not been submited."
			link = "./guestRegister"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error':err , 'link':link}))
		
		try:
			validate_email(email)
			valid_email = True
		except:
			valid_email = False
		if not valid_email:
			err = "Email address is not valid."
			link = "./guestRegister"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error':err , 'link':link}))
		if request.POST.get('password') != request.POST.get('passwordR'):
			err = "Passwords do not match"
			link = "./guestRegister"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error':err , 'link':link}))
		if not bool(request.POST.get('name', False)):
			err = "Name has not been submited"
			link = "./guestRegister"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error':err , 'link':link}))
		if not bool(request.POST.get('surname', False)):
			err = "Surname has not been submited"
			link = "./guestRegister"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error':err , 'link':link}))
		if not bool(request.POST.get('address', False)):
			err = "Address has not been submited"
			link = "./guestRegister"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error':err , 'link':link}))
		##############################################################################
		geolocator = Nominatim()
		try:
			location = geolocator.geocode(request.POST.get('address'))
		except:
			err = "Address could not be located at this moment."
			link = "./guestRegister"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error':err , 'link':link}))
		if location is None:
			error = 'Address could not be located, try using your countrys language.'
			link = "./GuestProfile"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		try:
			user = User.objects.create_user(username = email, password = request.POST.get('password'))
			user.first_name="GUEST"
			user.save()
			guest = Guest.objects.create(user=user, name=request.POST.get('name'), surname=request.POST.get('surname'), address=request.POST.get('address'), email=request.POST.get('email'),activated=False, lat=location.latitude, long=location.longitude)
		except IntegrityError:
			err = "E-mail already exists"
			link = "./"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error':err , 'link':link}))
		#Slanje email-a
		_thread.start_new_thread(sendEmail, (email,guest.id))
		template = loader.get_template("static/completeReg.html")
		return HttpResponse(template.render())
#slanje mail-a pri registraciji
def sendEmail(email,id):
	fromaddr = "tp4restoranii@gmail.com"
	toaddr = email
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Registration to restoraniiTP4"
	
	body = "<html><head></head><body>Welcome, to complete registration please open <a href= http:/localhost:8000/restoranii/activate?id="+str(id)+">link</a> in a new page</body></html>"
	msg.attach(MIMEText(body, 'html'))
	
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "restorani")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
#aktivacija preko maila
def activateGuest(request):
	if request.method=='GET':
		id = request.GET.get('id')
		guest = Guest.objects.get(pk=id)
		guest.activated = True
		guest.save()
		template = loader.get_template("static/completeActivation.html")
		return HttpResponse(template.render())
#uslov za pristup stranici kao gost
def guestCheck(user):
	return user.first_name=="GUEST"
#home stranica za goste
@login_required(redirect_field_name='IndexPage')
@user_passes_test(guestCheck,login_url='./')
def guestPage(request):
	template = loader.get_template("guestHomepage.html")
	reservations = Reservation.objects.filter(guest__pk = request.user.guest.id)
	return HttpResponse(template.render({'visits':reservations}))

#friends
@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(guestCheck,login_url='./')
def friends(request):
	if request.method=="GET":
		text = request.GET.get('starts')
		if text is None:
			text = ""
		friendList = request.user.guest.friends.filter(Q(name__startswith=text)|Q(surname__startswith=text))
		template = loader.get_template("friends.html")
		return HttpResponse(template.render({'friends':friendList , 'filter':text}))
	if request.method=="POST":
		if request.POST.get("type")=='add':
			try:
				friend = Guest.objects.get(email=request.POST.get('email'))
				request.user.guest.friends.add(friend)
				return redirect('friendsList')
			except:
				err = "No user with such email address."
				link = "./Friends"
				template = loader.get_template("error.html")
				return HttpResponse(template.render({'error':err , 'link':link}))
		else:
			friend = Guest.objects.get(id=request.POST.get("identity"))
			request.user.guest.friends.remove(friend)
			return redirect('friendsList')
		

#restaurant list
@login_required(redirect_field_name='IndexPage')
@user_passes_test(guestCheck,login_url='./')
def restaurantList(request):
	type = request.GET.get('sort')
	way = request.GET.get('asc')
	distance = {}
	rats = {}
	frats = {}
	restaurants = Restaurant.objects.defer("name","id","type","address","lat","long")
	#svi za rating prijatelja
	peopleList = []
	peopleList.append(request.user.guest.id)
	for friend in request.user.guest.friends.all():
		peopleList.append(friend)
	#proracunaj distancu i rejting za svaki restoran
	for rest in restaurants:
		ratings = RatingRestaurant.objects.filter(restaurant=rest)
		
		avrRate = 0
		avrFRate = 0
		numr = 0
		numfr = 0
		
		for rating in ratings:
			avrRate = avrRate + rating.rating
			numr = numr + 1
			if rating.guest.id in peopleList:
				avrFRate = avrFRate + rating.rating
				numfr = numfr + 1
		if numr!=0:
			avrRate = avrRate/numr
		if numfr!=0:
			avrFRate = avrFRate/numfr
		
		rats[rest.id]=avrRate
		frats[rest.id]=avrFRate
		distance[rest.id]=vincenty((request.user.guest.lat, request.user.guest.long), (rest.lat,rest.long)).kilometers
	
	if type is None:
		type="name"
	if way is None:
		way="asc"
	if type=="name":
		if way=="asc":
			sortedRestaurants = sorted(restaurants, key= lambda restaurant: restaurant.name.lower())
		if way=="des":
			sortedRestaurants = sorted(restaurants, key= lambda restaurant: restaurant.name.lower(),reverse=True)
	if type=="type":
		if way=="asc":
			sortedRestaurants = sorted(restaurants, key= lambda restaurant: restaurant.type.lower())
		if way=="des":
			sortedRestaurants = sorted(restaurants, key= lambda restaurant: restaurant.type.lower(),reverse=True)
	if type=="distance":
		if way=="asc":
			sortedRestaurants = sorted(restaurants, key= lambda restaurant: distance[restaurant.id])
		if way=="des":
			sortedRestaurants = sorted(restaurants, key= lambda restaurant: distance[restaurant.id],reverse=True)
	if type=="rating":
		if way=="asc":
			sortedRestaurants = sorted(restaurants, key= lambda restaurant: rats[restaurant.id])
		if way=="des":
			sortedRestaurants = sorted(restaurants, key= lambda restaurant: rats[restaurant.id],reverse=True)
	if type=="frating":
		if way=="asc":
			sortedRestaurants = sorted(restaurants, key= lambda restaurant: frats[restaurant.id])
		if way=="des":
			sortedRestaurants = sorted(restaurants, key= lambda restaurant: frats[restaurant.id],reverse=True)
	print(distance)
	template = loader.get_template("restaurantList.html")
	return HttpResponse(template.render({'restaurants':sortedRestaurants,'distances':distance, 'ratings':rats, 'fratings':frats}))
#profile
@login_required(redirect_field_name='IndexPage')
@user_passes_test(guestCheck,login_url='./')
def profile(request):
	template = loader.get_template("guestProfile.html")
	return HttpResponse(template.render({'name':request.user.guest.name,'surname':request.user.guest.surname,'email':request.user.guest.email,'address':request.user.guest.address}))
	
#edit profile data
@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(guestCheck,login_url='./')
def editprofile(request):
	change = request.POST.get('type')
	if change=='n':
		user = Guest.objects.only("name").get(id = request.user.guest.id)
		user.name = request.POST.get('name')
		user.save()
	if change=='s':
		user = Guest.objects.only("surname").get(id = request.user.guest.id)
		user.surname = request.POST.get('surname')
		user.save()
	if change=='a':
		geolocator = Nominatim()
		try:
			location = geolocator.geocode(request.POST.get('address'))
		except:
			err = "Address could not be located at this moment."
			link = "./GuestProfile"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error':err , 'link':link}))
		if location is None:
			error = 'Address could not be located, try using your countrys language.'
			link = "./GuestProfile"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		user = Guest.objects.only("address","long","lat").get(id = request.user.guest.id)
		user.address = request.POST.get('address')
		user.long = location.longitude
		user.lat = location.latitude
		user.save()
	if change=='p':
		if authenticate(request, username=request.user.guest.email, password=request.POST.get('opass')) is not None:
			if request.POST.get('pass')==request.POST.get('rpass') and request.POST.get('pass')!="":
				request.user.set_password(request.POST.get('pass'))
				request.user.save()
				login(request,request.user)
			else:
				err = "Passwords do not match."
				link = "./GuestProfile"
				template = loader.get_template("error.html")
				return HttpResponse(template.render({'error':err , 'link':link}))
		else:
			err = "Current password is not correct."
			link = "./GuestProfile"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error':err , 'link':link}))
	return redirect('profileOfGuest')
@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(guestCheck,login_url='./')
def res_part1(request):
	rest = Restaurant.objects.only("id","name").get(id=request.POST.get('identity'))
	template = loader.get_template("reservation.html")
	return HttpResponse(template.render({'name':rest.name,'id':rest.id}))
@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(guestCheck,login_url='./')
def res_part2(request):
	tlist = []
	dandt = request.POST.get('dandt').split('T')[0] +' '+ request.POST.get('dandt').split('T')[1]
	duration = request.POST.get('duration')
	startTime = dandt
	endTime = add_time(dandt,int(duration))
	restaurant = Restaurant.objects.get(id = request.POST.get('identity'))
	tables = RestaurantTable.objects.filter(restaurant = restaurant)
	#Kroz celu velicinu restorana
	for i in range(restaurant.sizeX):
		for j in range(restaurant.sizeY):
			test = True
			#za stolove koji postoje
			if tables is not None:
				for table in tables:
					#za pronadjeni sto na datoj poziciji
					if i==table.posX and j==table.posY:
						tableH = TableHelp()
						#preuzmi rezervacije za taj sto, koje su aktivne u datom restoranu
						reservations = Reservation.objects.only("date","duration").filter(restaurant= restaurant, complete = False, restaurantTables__id=table.id)
						#ako ih nema onda je sto slobodan
						if reservations is None:
							tableH.status = True
						#ako ih ima treba proveriti
						else:
							test2 = True
							#za svaku rezervaciju
							for resr in reservations:
								#sa pocetkom i krajem
								tableStart = str(resr.date)
								tableEnd = add_time(tableStart,resr.duration)
								#proveri da li rezervacija pocinje pre kraja moje i da li se zavrsava nakon mog pocetka
								if tableStart <= endTime and tableEnd >= startTime:
									#ako da sto je iskljucen
									tableH.status = False
									test2 = False
							if test2:
								tableH.status = True
						#ostatak koda :)
						tableH.posX=i
						tableH.posY=j
						tableH.num = table.tableNo
						tableH.segment = table.segment.name
						tableH.id = table.id
						tableH.chairs = table.chairNo
						tlist.append(tableH)
						test = False
			#i ako ih nema
			if test:
				tableH = TableHelp()
				tableH.posX=i
				tableH.posY=j
				tableH.status = False
				tableH.num = ""
				tableH.segment = ""
				tableH.chairs = 0
				tableH.id = -1
				tlist.append(tableH)
	template = loader.get_template("restablepick.html")
	return HttpResponse(template.render({'name':restaurant.name,'id':restaurant.id,'dandt':dandt,'duration':duration,'tables':tlist,'listI':list(range(0, restaurant.sizeX)),'listJ':list(range(0,restaurant.sizeY))}))
	
@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(guestCheck,login_url='./')
def res_part3(request):
	tids = request.POST.get('tableIds')
	if tids=="":
		err = "No tables selected."
		link = "./guestHomePage"
		template = loader.get_template("error.html")
		return HttpResponse(template.render({'error':err , 'link':link}))
	dandt = request.POST.get('dandt')
	duration = request.POST.get('duration')
	restaurant = Restaurant.objects.get(id = request.POST.get('identity'))
	chairNo = request.POST.get('chairs')
	tableNums = ""
	for id in tids.split():
		table = RestaurantTable.objects.get(id = id)
		if table is not None:
			tableNums += " "+str(table.tableNo)
	
	template = loader.get_template("friendPick.html")
	friends = request.user.guest.friends.all()
	return HttpResponse(template.render({'name':restaurant.name,'id':restaurant.id,'dandt':dandt,'duration':duration,'tableIds':tids,'chairNo':chairNo,'tableNums':tableNums,'friends':friends}))

@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(guestCheck,login_url='./')
def res_part4(request):
	rtableslist = []
	tids = request.POST.get('tableIds')
	dandt = request.POST.get('dandt')
	duration = request.POST.get('duration')
	restaurant = Restaurant.objects.get(id = request.POST.get('identity'))
	friends = request.POST.get('friends')
	flist = friends.split(' ')
	tlist = tids.split(' ')
	if len(flist) > 1:
		flist = flist[1:]
	else:
		flist = None
	if len(tlist) > 1:
		tlist = tlist[1:]
	else:
		tlist = None
	reservation = Reservation(restaurant = restaurant,complete=False,date = dandt,duration=duration)
	if tlist is not None:
		for tid in tlist:
			table = RestaurantTable.objects.get(id=tid)
			rtableslist.append(table)
	startTime = dandt
	endTime = add_time(dandt,int(duration))
	#imam rezervaciju, zakljucati sto, proveriti da li je validna, ubaciti i otkljucati sto
	cursor = connection.cursor()
	#zakljucano
	cursor.execute("LOCK TABLES restorani_reservation WRITE,restorani_reservation_restaurantTables WRITE")
	#svi stolovi koje hocemo da rezervisemo
	for table in rtableslist:
		#izvadimo rezervacije koje imaju id stola, za taj restoran i aktivne su
		reservations = Reservation.objects.only("date","duration").filter(restaurant= restaurant, complete = False, restaurantTables__id=table.id)
		#ako ih nema onda je sto slobodan
		if reservations is None:
			pass
		#ako ih ima treba proveriti
		else:
			#za svaku rezervaciju
			for resr in reservations:
				#sa pocetkom i krajem
				tableStart = str(resr.date)
				tableEnd = add_time(tableStart,resr.duration)
				#proveri da li rezervacija pocinje pre kraja moje i da li se zavrsava nakon mog pocetka
				if tableStart <= endTime and tableEnd >= startTime:
					#ako da sto je nedostupan
					#otkljucaj
					cursor.execute("UNLOCK TABLES;")
					err = "Jedan od izabranih stolova je u međuvremenu rezervisan."
					link = "./"
					template = loader.get_template("error.html")
					return HttpResponse(template.render({'error':err , 'link':link}))
	#otkljucano
	cursor.execute("UNLOCK TABLES;")
	reservation.save()
	request.user.guest.reservations.add(reservation)
	if tlist is not None:
		for tid in tlist:
			table = RestaurantTable.objects.get(id=tid)
			reservation.restaurantTables.add(table)
	invList = InviteList(reservation = reservation)
	invList.save()
	if flist is not None:
		for fid in flist:
			friend = Guest.objects.get(id=fid)
			invList.guests.add(friend)
	for guest in invList.guests.all():
		_thread.start_new_thread(sendEmailRes, (guest.email,reservation.id,restaurant.name))
	return redirect('guestHomePage')
	
@login_required(redirect_field_name='IndexPage')
@user_passes_test(guestCheck,login_url='./')	
def res_page(request):
	if request.method=='GET':
		id = request.GET.get('id')
		reservation = Reservation.objects.get(pk=id)
		try:
			guest = reservation.invitelist.guests.get(id = request.user.guest.id)
		except:
			error = 'You are not invited to join this reservation.'
			link = "./guestHomePage"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		tnum = ""
		for table in reservation.restaurantTables.all():
			tnum = tnum + " " + str(table.tableNo)
		date = str(reservation.date)
		duration = str(reservation.duration)
		rname = reservation.restaurant.name
		template = loader.get_template("reservationchoice.html")
		return HttpResponse(template.render({'name':rname,'dandt':date,'duration':duration,'tableNums':tnum,'id':reservation.id}))
	

@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(guestCheck,login_url='./')
def res_confirm(request):
	if request.method=='POST':
		id = request.POST.get('id')
		reservation = Reservation.objects.get(pk=id)
		try:
			guest = reservation.invitelist.guests.get(id = request.user.guest.id)
		except:
			error = 'You are not invited to join this reservation.'
			link = "./guestHomePage"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		guest.reservations.add(reservation)
		reservation.invitelist.guests.remove(guest)
		return redirect('guestHomePage')
@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(guestCheck,login_url='./')
def res_deny(request):
	if request.method=='POST':
		id = request.POST.get('id')
		reservation = Reservation.objects.get(pk=id)
		try:
			guest = reservation.invitelist.guests.get(id = request.user.guest.id)
		except:
			error = 'You are not invited to join this reservation.'
			link = "./guestHomePage"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		reservation.invitelist.guests.remove(guest)
		return redirect('guestHomePage')

@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(guestCheck,login_url='./')
def order_food(request):
	if request.method=='GET':
		id = request.GET.get('id')
		res = Reservation.objects.get(id = int(id))
		food = Food.objects.filter(restaurant=res.restaurant)
		drinks = Beaverage.objects.filter(restaurant=res.restaurant)
		template = loader.get_template("orderFoodGuest.html")
		return HttpResponse(template.render({'res': res, 'food': food, 'drinks': drinks, 'tables':res.restaurantTables.all()}))
	if request.method=='POST':
		id = request.POST.get('id')
		reservation = Reservation.objects.get(id = int(id))
		if reservation.date<timezone.now():
			error = 'You cannot use online order anymore.'
			link = "./guestHomePage"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': error, 'link': link}))
		tableNumber = request.POST.get('tableNo')
		orderedFood = request.POST.get('foods')
		orderedDrinks = request.POST.get('drinks')
		orderedFood = orderedFood.strip()
		orderedDrinks = orderedDrinks.strip()
		food = orderedFood.split(' ')
		drinks = orderedDrinks.split(' ')
		e = Waiter.objects.filter(restaurant = reservation.restaurant)[0]
		em = []
		em.append(e)
		rest = e.restaurant
		t = RestaurantTable.objects.get(tableNo=tableNumber, restaurant=rest)
		order = Order.objects.create(table=t, paid=False)
		order.save()
		foodList = []
		foodDict = {}
		for i in food:
			f = Food.objects.get(id=i)
			foodDict[f] = 0
		for i in food:
			f = Food.objects.get(id=i)
			foodDict[f] += 1
		for key in foodDict:
			of = OrderedFood.objects.create(food=key, amount=foodDict[key])
			of.save()
			foodList.append(of)
		drinkList = []
		drinkDict = {}
		for i in drinks:
			d = Beaverage.objects.get(id=i)
			drinkDict[d] = 0
		for j in drinks:
			d = Beaverage.objects.get(id=j)
			drinkDict[d] += 1
		for key in drinkDict:
			od = OrderedDrink.objects.create(beaverage=key, amount=drinkDict[key])
			od.save()
			drinkList.append(od)
		order.ordereddrinks = drinkList
		order.orderedfoods = foodList
		order.employees = em
		order.time = str(reservation.date)
		order.save()
		template = loader.get_template("static/finishedOrder.html")
		return HttpResponse(template.render())
@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(guestCheck,login_url='./')
def rate(request):
	if request.method=='GET':
		id = request.GET.get('id')
		reservation = Reservation.objects.get(id=id)
		template = loader.get_template("rate.html")
		return HttpResponse(template.render({'id':id,'name':reservation.restaurant.name}))
	if request.method=='POST':
		id = request.POST.get('id')
		rgrade = request.POST.get('restaurant')
		wgrade = request.POST.get('service')
		fgrade = request.POST.get('food')
		reservation = Reservation.objects.get(id=id)
		restaurant = reservation.restaurant
		RatingRestaurant.objects.create(restaurant = restaurant,guest = request.user.guest, rating = int(rgrade))
		#ocenjivanje konobara ispod
		date = str(reservation.date).split(' ')
		time = date[1]
		date = date[0]
		if time>='08:00' and time<='15:59':
			shift = 1
		if time>='16:00' and time<='23:59':
			shift = 2
		if time>='00:00' and time<='07:59':
			shift = 3
		try:
			sch = Schedule.objects.filter(shift = shift, date = date)
			for s in sch:
				RatingServices.objects.create(employee = s.employee, rating = int(wgrade))
		except:
			pass
		#ocenjivanje hrane ispod
		try:
			ord = Order.objects.filter(time = str(reservation.date))
			for o in ord:
				for foodO in o.orderedfoods.all():
					RatingFood.objects.create(food = foodO.food, rating = int(fgrade))
		except:
			pass
		#kraj ocenjivanja
		reservation.rated = True
		reservation.save()
		return redirect("guestHomePage")
	
@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(guestCheck,login_url='./')	
def cancel_res(request):
	if request.method=='POST':
		id = request.POST.get('id')
		reservation = Reservation.objects.get(id = int(id))
		request.user.guest.reservations.remove(reservation)
		return redirect("guestHomePage")
	
def sendEmailRes(email,id,rName):
	fromaddr = "tp4restoranii@gmail.com"
	toaddr = email
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Invite for reservation to "+rName
	
	body = "<html><head></head><body>You have been invited to join restaurant reservation, to confirm or declain please open this <a href= http:/localhost:8000/restoranii/confirmReservation?id="+str(id)+">link</a> in a new page. You need to be signed in to access this page.</body></html>"
	msg.attach(MIMEText(body, 'html'))
	
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "restorani")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

def add_time(date,hour):
	dt = datetime(day = int(date.split(' ')[0].split('-')[2]),month = int(date.split(' ')[0].split('-')[1]), year = int(date.split(' ')[0].split('-')[0]), hour = int(date.split(' ')[1].split(':')[0]), minute = int(date.split(' ')[1].split(':')[1]))
	dt = dt + timedelta(hours=hour)
	result = str(dt)
	result = result.split(':')[0]+':'+result.split(':')[1]
	return result
	
@register.filter
def get_item(dict,key):
	return dict.get(key)
@register.filter
def get_stars(dict,key):
	val = dict.get(key)
	if val is None:
		return "-"
	if val<0.5:
		return "-"
	if val<1:
		return "•"
	if val<1.5:
		return "⚹"
	if val<2:
		return "⚹•"
	if val<2.5:
		return "⚹⚹"
	if val<3:
		return "⚹⚹•"
	if val<3.5:
		return "⚹⚹⚹"
	if val<4:
		return "⚹⚹⚹•"
	if val<4.5:
		return "⚹⚹⚹⚹"
	if val<5:
		return "⚹⚹⚹⚹•"
	return "⚹⚹⚹⚹⚹"
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from restorani.models import Guest
from restorani.models import Reservation
from restorani.models import Restaurant
from restorani.models import RestaurantTable
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
from restorani.models import RatingRestaurant
from validate_email import validate_email
from restorani.models import TableHelp
from datetime import datetime, timedelta

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
	reservations = Reservation.objects.defer("restaurantTables").filter(guest= request.user.guest)
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
		ratings = RatingRestaurant.objects.filter(id=rest.id)
		
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
	endTime = add_time(dandt,3)
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
								tableStart = resr.date
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
	print(str(request.POST.get('tableIds')))
	print(1)
	return HttpResponse("Done")

@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(guestCheck,login_url='./')
def res_part4(request):
	pass
	
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
		return "'"
	if val<1.5:
		return "*"
	if val<2:
		return "*'"
	if val<2.5:
		return "**"
	if val<3:
		return "**'"
	if val<3.5:
		return "***"
	if val<4:
		return "***'"
	if val<4.5:
		return "****"
	if val<5:
		return "****'"
	return "*****"
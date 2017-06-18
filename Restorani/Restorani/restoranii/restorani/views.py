from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import smtplib
import _thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from restorani.models import Guest
from restorani.models import Restaurant
from restorani.models import RestaurantManager
from restorani.models import Employee
from restorani.models import Cook
from restorani.models import Waiter
from restorani.models import Bartender
from django.db import IntegrityError
from django.contrib.auth.decorators import user_passes_test,login_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
#///SVI///#
#Go To Index funkcija
def index(request):
	if not request.user.is_authenticated():
		template = loader.get_template("static/guestLogin.html")
		return HttpResponse(template.render())
	else:
		#ovde uneti tonu ifova za svaki tip korisnika koji ima razlicitu pocetnu stranicu
		if request.user.first_name=="GUEST":
			if request.user.guest.activated==False:
				return redirect("logOut")
			return redirect("guestHomePage")
		if (request.user.first_name == "SYSTEM"):
			return redirect("SMHomePage")
		if (request.user.first_name == "MANAGER"):
			return redirect("RMHomePage")
		if (request.user.first_name == "COOK"):
			return redirect("cookHomePage")
		if (request.user.first_name == "BARTENDER"):
			return redirect("bartenderHomePage")
		if (request.user.first_name == "WAITER"):
			return redirect("waiterHomePage")
@csrf_exempt
#LogInFunkcija
def loginRequest(request):
	userEmail = request.POST.get('email',False)
	userPass = request.POST.get('password',False)
	if not bool(userEmail):
		err = "Email has not been submited."
		link = "./"
		template = loader.get_template("error.html")
		return HttpResponse(template.render({'error':err , 'link':link}))
	if not bool(userPass):
		err = "Password has not been submited."
		link = "./"
		template = loader.get_template("error.html")
		return HttpResponse(template.render({'error':err , 'link':link}))
	user = authenticate(request, username=userEmail, password=userPass)
	if user is not None:
		login(request, user)
		return redirect("IndexPage")
	else:
		err = "User with that email/password combination does not exist."
		link = "./"
		template = loader.get_template("error.html")
		return HttpResponse(template.render({'error':err , 'link':link}))
#LogOutFunkcija
@login_required(redirect_field_name='IndexPage')
def logOut(request):
	logout(request)
	return redirect("IndexPage")
#///////////#
#///GOSTI///#
#Registracija Gostiju
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
		try:
			user = User.objects.create_user(username = email, password = request.POST.get('password'))
			user.first_name="GUEST"
			user.save()
			guest = Guest.objects.create(user=user, name=request.POST.get('name'), surname=request.POST.get('surname'), address=request.POST.get('address'), email=request.POST.get('email'),activated=False)
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
@user_passes_test(guestCheck,login_url='./')
def guestPage(request):
	template = loader.get_template("static/guestHomeTmp.html")
	return HttpResponse(template.render({'Email':request.user.guest.email}))

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////
#uslov za pristump stranici kao menadzer sistema
def SystemManCheck(systemManager):
	return systemManager.first_name=="SYSTEM"
#home stranica za menagera sistema
@user_passes_test(SystemManCheck,login_url='./')
def SystemManPage(request):
	template = loader.get_template("static/SMHomePage.html")
	return HttpResponse(template.render())

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////
#uslov za pristump stranici kao menadzer restorana
def restaurantManagerCheck(restaurantManager):
	return restaurantManager.first_name=="MANAGER"
#home stranica za menagera sistema
@user_passes_test(restaurantManagerCheck,login_url='./')
def restaurantManagerCheck(request):
	template = loader.get_template("static/RMHomePage.html")
	return HttpResponse(template.render())

#registracija novog restorana
@csrf_exempt
def registarRestaurant(request):
	if request.method == 'GET':
		template = loader.get_template("static/restaurantReg.html")
		return HttpResponse(template.render())
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
		restaurant = Restaurant.objects.create(name = request.POST.get('name'), type = request.POST.get('type'), address =request.POST.get('address') , sizeX = request.POST.get('dimX'), sizeY = request.POST.get('dimY'))
		template = loader.get_template("static/success.html")
		return HttpResponse(template.render())

#///////////////////////////////////////////////////////////////////////////////////////////////
#registracija menadzera restorana
@csrf_exempt
def registarRestaurantMan(request):
	if request.method == 'GET':
		list = Restaurant.objects.all()
		template = loader.get_template("restaurantManReg.html")
		return HttpResponse(template.render({'lista':list}))
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
		template = loader.get_template("static/success.html")
		return HttpResponse(template.render())

#/////////////////////////////////////////////////////////////////////////////////////////////
@csrf_exempt
def registarEmployee(request):
	if request.method == 'GET':
		list = Restaurant.objects.all()
		template = loader.get_template("employeeReg.html")
		return HttpResponse(template.render({'lista': list}))
	if request.method == 'POST':
		restaurantID = Restaurant.objects.get(name=request.POST.get('r'))
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

		template = loader.get_template("static/success.html")
		return HttpResponse(template.render())
###############################################################################
#Uslova za pristup stranicama kao odedjeni zaposleni radnik
def cookCheck(employee):
	return employee.first_name=="COOK"
def bartenderCheck(employee):
	return employee.first_name=="BARTENDER"
def waiterCheck(employee):
	return employee.first_name=="WAITER"
################################################################
#home stranica za kuvara
@user_passes_test(cookCheck,login_url='./')
def cookPage(request):
	if(request.user.last_name == "False"):
		template = loader.get_template("cookHomePage.html")
		return HttpResponse(template.render())
	else:
		template = loader.get_template("static/firstLoginPasswordChange.html")
		return HttpResponse(template.render())
###################################################################
#home stranica za sankera
@user_passes_test(bartenderCheck,login_url='./')
def bartenderPage(request):
	if(request.user.last_name == "False"):
		template = loader.get_template("bartenderHomePage.html")
		return HttpResponse(template.render())
	else:
		template = loader.get_template("static/firstLoginPasswordChange.html")
		return HttpResponse(template.render())
###################################################################
#home stranica za konobara
@user_passes_test(waiterCheck,login_url='./')
def waiterPage(request):
	if(request.user.last_name == "False"):
		template = loader.get_template("waiterHomePage.html")
		return HttpResponse(template.render())
	else:
		template = loader.get_template("static/firstLoginPasswordChange.html")
		return HttpResponse(template.render())
#########################################################
@csrf_exempt
def firstLogin(request):
	password = request.POST.get('password', False)
	repeatPass = request.POST.get('passwordR', False)
	if not password:
		err = "Password has not been submited."
		link = "./changePassword"
		template = loader.get_template("error.html")
		return HttpResponse(template.render({'error': err, 'link': link}))
	if not repeatPass:
		err = "Repeat Password has not been submited."
		link = "./changePassword"
		template = loader.get_template("error.html")
		return HttpResponse(template.render({'error': err, 'link': link}))
	if (password == repeatPass):
		if(request.user.first_name == "COOK"):
			request.user.set_password(password);
			request.user.last_name = False
			request.user.save()
			template = loader.get_template("cookHomePage.html")
			return HttpResponse(template.render())
		if (request.user.first_name == "BARTENDER"):
			request.user.set_password(password);
			request.user.last_name = False
			request.user.save()
			template = loader.get_template("bartenderHomePage.html")
			return HttpResponse(template.render())
		if (request.user.first_name == "WAITER"):
			request.user.set_password(password);
			request.user.last_name = False
			request.user.save()
			template = loader.get_template("waiterHomePage.html")
			return HttpResponse(template.render())
	else:
		err = "Passwords do not match!"
		link = "./changePassword"
		template = loader.get_template("error.html")
		return HttpResponse(template.render({'error': err, 'link': link}))
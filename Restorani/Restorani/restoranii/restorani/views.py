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
		if(request.user.first_name=="GUEST"):
			return redirect("guestHomePage")
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
@login_required
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
def guestCheck(guest):
	return guest.first_name=="GUEST"
#home stranica za goste
@user_passes_test(guestCheck,login_url='./')
def guestPage(request):
	template = loader.get_template("static/guestHomeTmp.html")
	return HttpResponse(template.render())

#//////////////#

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import user_passes_test,login_required
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from restorani.models import SystemManager

# Create your views here.
#///SVI///#
#Go To Index funkcija, odlazi na pocetnu stranicu koja odgovara liku, tako da slobodno je pozivajte
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
#Promena sifre pri prvom logovanju
@csrf_exempt
@login_required(redirect_field_name='IndexPage')
def firstLogin(request):
	password = request.POST.get('password', False)
	repeatPass = request.POST.get('passwordR', False)
	if (request.user.first_name == "COOK"):
		template = loader.get_template("cookHomePage.html")
		link = "./cookHomePage"
	if (request.user.first_name == "BARTENDER"):
		template = loader.get_template("bartenderHomePage.html")
		link = "./bartenderHomePage"
	if (request.user.first_name == "WAITER"):
		template = loader.get_template("waiterHomePage.html")
		link = "./waiterHomePage"
	if not password:
		err = "Password has not been submited."
		template = loader.get_template("error.html")
		return HttpResponse(template.render({'error': err, 'link': link}))
	if not repeatPass:
		err = "Repeat Password has not been submited."
		link = "./changePassword"
		template = loader.get_template("error.html")
		return HttpResponse(template.render({'error': err, 'link': link}))

	if (password == repeatPass):
		request.user.set_password(password);
		request.user.last_name = False
		request.user.save()
		return HttpResponse(template.render())
	else:
		err = "Passwords do not match!"
		template = loader.get_template("error.html")
		return HttpResponse(template.render({'error': err, 'link': link}))
@csrf_exempt	
def sysAdmin(request):
	user = User.objects.create_user(username = 'admin@admin.com', password = 'admin')
	user.first_name="SYSTEM"
	user.save()
	SystemManager.objects.create(user=user, email= 'admin@admin.com', name="Admin",surname="Adminovic")
	return HttpResponse("<html><head></head><body>Done</body></html>")
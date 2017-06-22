from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from restorani.models import Guest
from restorani.models import Reservation
from restorani.models import Restaurant
import smtplib
import _thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.decorators import user_passes_test,login_required
from django.views.decorators.csrf import csrf_exempt

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
	template = loader.get_template("guestHomepage.html")
	reservations = Reservation.objects.defer("restaurantTables").filter(guest= request.user.guest)
	return HttpResponse(template.render({'visits':reservations}))

#friends
@csrf_exempt
@user_passes_test(guestCheck,login_url='./')
def friends(request):
	if request.method=="GET":
		friendList = request.user.guest.friends.all()
		template = loader.get_template("friends.html")
		return HttpResponse(template.render({'friends':friendList}))
	if request.method=="DELETE":
		pass
	if request.method=="POST":
		pass

#restaurant list
@user_passes_test(guestCheck,login_url='./')
def restaurantList(request):
	restaurants = Restaurant.objects.defer("name","id","type","address")
	template = loader.get_template("restaurantList.html")
	return HttpResponse(template.render({'restaurants':restaurants}))
#profile
@user_passes_test(guestCheck,login_url='./')
def profile(request):
	template = loader.get_template("guestProfile.html")
	return HttpResponse(template.render({'name':request.user.guest.name,'surname':request.user.guest.surname,'email':request.user.guest.email,'address':request.user.guest.address}))
	
#edit profile data
@csrf_exempt
@user_passes_test(guestCheck,login_url='./')
def editprofile(request):
	user = Guest.objects.only("name","surname","password"
	change = request.POST.get('type')
	if change=='n':
		
	if change=='s':
	if change=='e':
	if change=='a':
	if change=='p':
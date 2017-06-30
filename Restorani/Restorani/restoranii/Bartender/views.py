from django.shortcuts import render
from restorani.models import Employee
from restorani.models import Bartender
from restorani.models import Order
from restorani.models import Notification
from restorani.models import Schedule
from django.template import loader
import datetime
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test,login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth import login

# Create your views here.

def bartenderCheck(employee):
	return employee.first_name=="BARTENDER"
	
@user_passes_test(bartenderCheck,login_url='./')
def bartenderPage(request):
	if(request.user.last_name == "False"):
		user = request.user.username
		b = Bartender.objects.get(email = user)
		restaurant = b.restaurant
		orders = Order.objects.all()
		temp = []
		for i in orders:
			if restaurant == i.table.restaurant:
				temp.append(i)

		s = Schedule.objects.all()
		sc = []
		for i in s:
			if i.employee.restaurant == restaurant and i.employee.user.first_name == "BARTENDER":
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
		template = loader.get_template("bartenderHomePage.html")
		return HttpResponse(template.render({'user': user,'orders':temp,"calendar":calendar,'shift1': shift1,'shift2': shift2,'shift3': shift3}))
	else:
		template = loader.get_template("static/firstLoginPasswordChange.html")
		return HttpResponse(template.render())


@user_passes_test(bartenderCheck,login_url='./')
def bartenderProfile(request):
	bartender = Bartender.objects.get(email=request.user.username)
	link = "./bartenderHomePage"
	template = loader.get_template("bartenderProfile.html")
	return HttpResponse(template.render({'bartender': bartender, 'back': link}))

@user_passes_test(bartenderCheck,login_url='./')
@csrf_exempt
def editBartenderProfile(request):
	bartender = Bartender.objects.get(email=request.user.username)
	bartender.name = request.POST.get('name')
	bartender.surname =request.POST.get('surname')
	if request.POST.get('size') is not None:
		bartender.size = request.POST.get('size')
	if request.POST.get('shoeSize') is not None:
		bartender.shoeSize = request.POST.get('shoeSize')
	bartender.save()
	return redirect('bartenderProfile')

@user_passes_test(bartenderCheck,login_url='./')
@csrf_exempt
def changeBartenderPassword(request):
	new = request.POST.get('newPass')
	repeat = request.POST.get('repPass')
	print(request.user.username)
	print(request.POST.get('oldPass'))
	print(request.user.password)
	if authenticate(request, username=request.user.username, password = request.POST.get('oldPass')) is not None:
		if new == repeat:
			request.user.set_password(new)
			request.user.save()
			login(request,request.user)
		else:
			err = "Passwords do not match."
			link = "./bartenderProfile"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': err, 'link': link}))
	else:
		err = "Current password is not correct."
		link = "./bartenderProfile"
		template = loader.get_template("error.html")
		return HttpResponse(template.render({'error': err, 'link': link}))
	return redirect('bartenderProfile')

@user_passes_test(bartenderCheck,login_url='./')
@csrf_exempt
def DrinkReady(request):
	orderID = request.POST.get('orderID')
	order = Order.objects.get(id = orderID)
	message = "Drinks Ready"
	type = "drink"
	n = Notification.objects.create(message = message,order = order, type = type)
	n.save()
	return redirect("bartenderHomePage")
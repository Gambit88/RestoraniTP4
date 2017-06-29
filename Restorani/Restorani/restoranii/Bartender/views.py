from django.shortcuts import render
from restorani.models import Employee
from restorani.models import Bartender
from restorani.models import Order
from django.template import loader
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
		template = loader.get_template("bartenderHomePage.html")
		return HttpResponse(template.render({'user': user,'orders':temp}))
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
from django.shortcuts import render
from django.template import loader
from restorani.models import Employee
from restorani.models import Waiter
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test,login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth import login

# Create your views here.
def waiterCheck(employee):
	return employee.first_name=="WAITER"
	
@user_passes_test(waiterCheck,login_url='./')
def waiterPage(request):
	if(request.user.last_name == "False"):
		user = request.user.username
		template = loader.get_template("waiterHomePage.html")
		return HttpResponse(template.render({'user': user}))
	else:
		template = loader.get_template("static/firstLoginPasswordChange.html")
		return HttpResponse(template.render())

@user_passes_test(waiterCheck,login_url='./')
def waiterProfile(request):
	waiter = Waiter.objects.get(email=request.user.username)
	link = "./waiterHomePage"
	template = loader.get_template("waiterProfile.html")
	return HttpResponse(template.render({'waiter': waiter, 'back': link}))

@user_passes_test(waiterCheck,login_url='./')
@csrf_exempt
def editWaiterProfile(request):
	waiter = Waiter.objects.get(email=request.user.username)
	waiter.name = request.POST.get('name')
	waiter.surname =request.POST.get('surname')
	if request.POST.get('size') is not None:
		waiter.size = request.POST.get('size')
	if request.POST.get('shoeSize') is not None:
		waiter.shoeSize = request.POST.get('shoeSize')
	waiter.save()
	return redirect('waiterProfile')

@user_passes_test(waiterCheck,login_url='./')
@csrf_exempt
def changeWaiterPassword(request):
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
			link = "./waiterProfile"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': err, 'link': link}))
	else:
		err = "Current password is not correct."
		link = "./waiterProfile"
		template = loader.get_template("error.html")
		return HttpResponse(template.render({'error': err, 'link': link}))
	return redirect('waiterProfile')
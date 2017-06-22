from django.shortcuts import render
from restorani.models import Employee
from restorani.models import Cook
from django.template import loader
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test,login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth import login

# Create your views here.
def cookCheck(employee):
	return employee.first_name=="COOK"
@user_passes_test(cookCheck,login_url='./')
def cookPage(request):
	if(request.user.last_name == "False"):
		user = request.user.username
		template = loader.get_template("cookHomePage.html")
		return HttpResponse(template.render({'user': user}))
	else:
		template = loader.get_template("static/firstLoginPasswordChange.html")
		return HttpResponse(template.render())

@user_passes_test(cookCheck,login_url='./')
def cookProfile(request):
	cook = Cook.objects.get(email=request.user.username)
	link = "./cookHomePage"
	template = loader.get_template("cookProfile.html")
	return HttpResponse(template.render({'cook':cook, 'back': link}))

@user_passes_test(cookCheck,login_url='./')
@csrf_exempt
def editCookProfile(request):
	cook = Cook.objects.get(email=request.user.username)
	cook.name = request.POST.get('name')
	cook.surname =request.POST.get('surname')
	cook.kind = request.POST.get('kind')
	if request.POST.get('size') is not None:
		cook.size = request.POST.get('size')
	if request.POST.get('shoeSize') is not None:
		cook.shoeSize = request.POST.get('shoeSize')
	cook.save()
	return redirect('cookProfile')

@user_passes_test(cookCheck,login_url='./')
@csrf_exempt
def changePassword(request):
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
			link = "./cookProfile"
			template = loader.get_template("error.html")
			return HttpResponse(template.render({'error': err, 'link': link}))
	else:
		err = "Current password is not correct."
		link = "./cookProfile"
		template = loader.get_template("error.html")
		return HttpResponse(template.render({'error': err, 'link': link}))
	return redirect('cookProfile')
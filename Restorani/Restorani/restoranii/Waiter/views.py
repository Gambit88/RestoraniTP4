from django.shortcuts import render
from django.template import loader
from restorani.models import Employee
from restorani.models import Waiter
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test,login_required

# Create your views here.
def waiterCheck(employee):
	return employee.first_name=="WAITER"
	
@user_passes_test(waiterCheck,login_url='./')
def waiterPage(request):
	if(request.user.last_name == "False"):
		template = loader.get_template("waiterHomePage.html")
		return HttpResponse(template.render())
	else:
		template = loader.get_template("static/firstLoginPasswordChange.html")
		return HttpResponse(template.render())
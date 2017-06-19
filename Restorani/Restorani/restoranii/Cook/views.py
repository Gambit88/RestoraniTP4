from django.shortcuts import render
from restorani.models import Employee
from restorani.models import Cook
from django.template import loader
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test,login_required

# Create your views here.
def cookCheck(employee):
	return employee.first_name=="COOK"
@user_passes_test(cookCheck,login_url='./')
def cookPage(request):
	if(request.user.last_name == "False"):
		template = loader.get_template("cookHomePage.html")
		return HttpResponse(template.render())
	else:
		template = loader.get_template("static/firstLoginPasswordChange.html")
		return HttpResponse(template.render())
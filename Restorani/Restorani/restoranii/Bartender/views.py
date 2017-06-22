from django.shortcuts import render
from restorani.models import Employee
from restorani.models import Bartender
from django.template import loader
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test,login_required

# Create your views here.

def bartenderCheck(employee):
	return employee.first_name=="BARTENDER"
	
@user_passes_test(bartenderCheck,login_url='./')
def bartenderPage(request):
	if(request.user.last_name == "False"):
		template = loader.get_template("bartenderHomePage.html")
		return HttpResponse(template.render())
	else:
		template = loader.get_template("static/firstLoginPasswordChange.html")
		return HttpResponse(template.render())

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


# Create your views here.
def index(request):
	template = loader.get_template("static/guestLogin.html")
	return HttpResponse(template.render())

def registerGuests(request):
	template = loader.get_template("static/guestRegister.html")
	return HttpResponse(template.render())
	
def regGuest(request):
	#fromaddr = "tp4restoranii@gmail.com"
	#toaddr = "ADDRESS YOU WANT TO SEND TO"
	#msg = MIMEMultipart()
	#msg['From'] = fromaddr
	#msg['To'] = toaddr
	#msg['Subject'] = "Registration to restoraniiTP4"
	
	#body = "Welcome, to complete registration please click on <a href= #http:/localhost:8000/restoranii/>link</a>"
	#msg.attach(MIMEText(body, 'plain'))
	
	#server = smtplib.SMTP('smtp.gmail.com', 587)
	#server.starttls()
	#server.login(fromaddr, "restorani")
	#text = msg.as_string()
	#server.sendmail(fromaddr, toaddr, text)
	#server.quit()
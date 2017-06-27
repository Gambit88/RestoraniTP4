from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import template
from django.contrib.auth.models import User
from django.template.defaulttags import register
from django.contrib.auth.decorators import user_passes_test,login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from restorani.models import Supplier
from restorani.models import Post
from restorani.models import Offer

def supplierCheck(supplier):
	return supplier.first_name=="SUPPLIER"

#home stranica za menagera sistema
@user_passes_test(supplierCheck,login_url='./')
def supplierHome(request):
	template = loader.get_template("supplierHomePage.html")
	supplier = Supplier.objects.get(email = request.user.username)
	return HttpResponse(template.render({'supplier': supplier}))

#prikaz svih ponuda i dodavanje ponude ponudjaca
@csrf_exempt
@user_passes_test(supplierCheck,login_url='./')
def allPosts(request):
    if request.method == "GET":
        try:
            allposts = Post.objects.filter(expiration_date__gte=timezone.now())
            template = loader.get_template("allPosts.html")
            return HttpResponse(template.render({'posts': allposts}))
        except:
            error = 'No current offers from managers'
            link = "supplierHomePage.html"
            template = loader.get_template("error.html")
            return HttpResponse(template.render({'error': error, 'link': link}))
    if request.method == "POST":
        supplier = Supplier.objects.get(email = request.user.username)
        post = Post.objects.get(pk = request.POST.get('addid'))
        o = Offer.objects.create(supplier = supplier, price = request.POST.get('price'), post = post, acepted = False)
        allposts = Post.objects.filter(expiration_date__gte=timezone.now())
        template = loader.get_template("allPosts.html")
        return HttpResponse(template.render({'posts': allposts}))

@csrf_exempt
@user_passes_test(supplierCheck,login_url='./')
def myOffers(request):
    try:
        print("//////////////")
        print("try")
        me = Supplier.objects.get(email=request.user.username)
        myoffers = Offer.objects.filter(supplier = me.pk)
        template = loader.get_template("myOffers.html")
        return HttpResponse(template.render({'offers': myoffers}))
    except:
        error = "You don't have any offers"
        link = "supplierHomePage.html"
        template = loader.get_template("error.html")
        return HttpResponse(template.render({'error': error, 'link': link}))


@csrf_exempt
@user_passes_test(supplierCheck,login_url='./')
def updateOffer(request):
    if request.method == "GET":
        offer = Offer.objects.get(pk=request.GET.get('addid'))
        template = loader.get_template("updateOffer.html")
        return HttpResponse(template.render({'offer': offer}))
    if request.method == "POST":
        offer = Offer.objects.get(pk=request.POST.get('addid'))
        offer.price = request.POST.get('newprice')
        offer.save()
        template = loader.get_template("updateOffer.html")
        return HttpResponse(template.render({'offer': offer}))


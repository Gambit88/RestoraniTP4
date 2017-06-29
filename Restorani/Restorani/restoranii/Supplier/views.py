from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import template
from django.contrib.auth.models import User
from django.template.defaulttags import register
from django.contrib.auth.decorators import user_passes_test,login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth import authenticate, login
from restorani.models import Supplier
from restorani.models import Post
from restorani.models import Offer

def supplierCheck(supplier):
	return supplier.first_name=="SUPPLIER"

#home stranica za menagera sistema
@login_required(redirect_field_name='IndexPage')
@user_passes_test(supplierCheck,login_url='./')
def supplierHome(request):
	template = loader.get_template("supplierHomePage.html")
	supplier = Supplier.objects.get(email = request.user.username)
	return HttpResponse(template.render({'supplier': supplier}))

#prikaz svih ponuda i dodavanje ponude ponudjaca
@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(supplierCheck,login_url='./')
def allPosts(request):
    if request.method == "GET":
        try:
            allOffers = Offer.objects.all()
            posts = Post.objects.all()
            list = []
            for i in posts:
                list.append(i)
            tempRemove = []
            for i in allOffers:
                if i.acepted:
                    tempRemove.append(i.post)
            for i in posts:
                if i.expiration_date <= timezone.now():
                    tempRemove.append(i)
            for i in tempRemove:
                for j in list:
                    if i == j:
                        list.remove(i)
            template = loader.get_template("allPosts.html")
            return HttpResponse(template.render({'posts': list}))
        except:
            error = 'No current offers from managers'
            link = "supplierHomePage.html"
            template = loader.get_template("error.html")
            return HttpResponse(template.render({'error': error, 'link': link}))
    if request.method == "POST":
        supplier = Supplier.objects.get(email = request.user.username)
        post = Post.objects.get(pk = request.POST.get('addid'))
        o = Offer.objects.create(supplier = supplier, price = request.POST.get('price'), post = post, acepted = False)
        allOffers = Offer.objects.all()
        posts = Post.objects.all()
        tempRemove = []
        for i in allOffers:
            if i.acepted:
                tempRemove.append(i.post)
        for i in posts:
            if i.expiration_date <= timezone.now():
                tempRemove.append(i)
        for i in tempRemove:
            posts.remove(i)
        template = loader.get_template("allPosts.html")
        return HttpResponse(template.render({'posts': posts}))

@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(supplierCheck,login_url='./')
def myOffers(request):
    try:
        me = Supplier.objects.get(email=request.user.username)
        myoffers = Offer.objects.filter(supplier = me.pk)
        allOffers = Offer.objects.all()
        tempAccepted = []
        myTemp = []
        # u tempAccepted se smestaju sve accepted offers
        # u myTemp sve offers ulogovanog supplier-a
        for i in allOffers:
            if i.acepted:
                tempAccepted.append(i)
            if i.supplier.email == request.user.username:
                myTemp.append(i)
        # tempRemove se dodaju svi offeri ciji su postovi jednaki sa accepted postovima
        tempRemove = []
        for i in myTemp:
            for j in tempAccepted:
                if i.post == j.post:
                    tempRemove.append(i)
            if i.post.expiration_date < timezone.now():
                tempRemove.append(i)
        # brisanje svih offera iz Myoffera ciji su postovi jednaki sa accepted postovima
        for i in tempRemove:
            myTemp.remove(i)


        template = loader.get_template("myOffers.html")
        return HttpResponse(template.render({'offers': myTemp}))
    except:
        error = "You don't have any offers"
        link = "supplierHomePage.html"
        template = loader.get_template("error.html")
        return HttpResponse(template.render({'error': error, 'link': link}))


@csrf_exempt
@login_required(redirect_field_name='IndexPage')
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

@csrf_exempt
@login_required(redirect_field_name='IndexPage')
@user_passes_test(supplierCheck,login_url='./')
def updateInfo(request):
    user = request.user.username
    supplier = Supplier.objects.get(email = request.user.username)
    if request.method == "POST":
        if not request.POST.get('name') and not request.POST.get('lastname') and not request.POST.get('opass') and not request.POST.get('rpass') and not request.POST.get('pass'):
            error = "You didn't input any changes"
            link = "updateInfo.html"
            template = loader.get_template("error.html")
            return HttpResponse(template.render({'error': error, 'link': link}))
        if request.POST.get('name'):
            supplier.name = request.POST.get('name')
        if request.POST.get('lastname'):
            supplier.surname = request.POST.get('lastname')
        if request.POST.get('opass') and request.POST.get('rpass') and request.POST.get('pass'):
            if authenticate(request, username=request.user.supplier.email, password=request.POST.get('opass')) is not None:
                if request.POST.get('pass') == request.POST.get('rpass') and request.POST.get('pass') != "":
                    request.user.set_password(request.POST.get('pass'))
                    request.user.save()
                    login(request, request.user)
                else:
                    err = "Passwords do not match."
                    link = "updateInfo.html"
                    template = loader.get_template("error.html")
                    return HttpResponse(template.render({'error': err, 'link': link}))
            else:
                err = "Current password is not correct."
                link = "updateInfo.html"
                template = loader.get_template("error.html")
                return HttpResponse(template.render({'error': err, 'link': link}))

        supplier.save()
    template = loader.get_template("updateInfo.html")
    return HttpResponse(template.render({'sup': supplier}))
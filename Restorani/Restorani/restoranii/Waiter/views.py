from django.shortcuts import render
from django.template import loader
from restorani.models import Employee
from restorani.models import Waiter
from restorani.models import RestaurantTable
from restorani.models import Food
from restorani.models import Beaverage
from restorani.models import Order
from restorani.models import OrderedFood
from restorani.models import OrderedDrink
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth import login


# Create your views here.
def waiterCheck(employee):
    return employee.first_name == "WAITER"


@user_passes_test(waiterCheck, login_url='./')
def waiterPage(request):
    if (request.user.last_name == "False"):
        user = request.user.username
        waiter = Waiter.objects.get(email=request.user.username)
        orders = Order.objects.filter(employees=waiter)
        template = loader.get_template("waiterHomePage.html")
        return HttpResponse(template.render({'user': user, 'order': orders}))
    else:
        template = loader.get_template("static/firstLoginPasswordChange.html")
        return HttpResponse(template.render())


@user_passes_test(waiterCheck, login_url='./')
def waiterProfile(request):
    waiter = Waiter.objects.get(email=request.user.username)
    link = "./waiterHomePage"
    template = loader.get_template("waiterProfile.html")
    return HttpResponse(template.render({'waiter': waiter, 'back': link}))


@user_passes_test(waiterCheck, login_url='./')
@csrf_exempt
def editWaiterProfile(request):
    waiter = Waiter.objects.get(email=request.user.username)
    waiter.name = request.POST.get('name')
    waiter.surname = request.POST.get('surname')
    if request.POST.get('size') is not None:
        waiter.size = request.POST.get('size')
    if request.POST.get('shoeSize') is not None:
        waiter.shoeSize = request.POST.get('shoeSize')
    waiter.save()
    return redirect('waiterProfile')


@user_passes_test(waiterCheck, login_url='./')
@csrf_exempt
def changeWaiterPassword(request):
    new = request.POST.get('newPass')
    repeat = request.POST.get('repPass')
    print(request.user.username)
    print(request.POST.get('oldPass'))
    print(request.user.password)
    if authenticate(request, username=request.user.username, password=request.POST.get('oldPass')) is not None:
        if new == repeat:
            request.user.set_password(new)
            request.user.save()
            login(request, request.user)
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


@user_passes_test(waiterCheck, login_url='./')
@csrf_exempt
def addOrder(request):  ##### IZBRISATI TESTIRANJE
    # waiter = request.user.employee
    waiter = Waiter.objects.get(email=request.user.username)
    restaurant = request.user.employee.restaurant
    tables = RestaurantTable.objects.filter(restaurant=restaurant)
    food = Food.objects.filter(restaurant=restaurant)
    drinks = Beaverage.objects.filter(restaurant=restaurant)
    template = loader.get_template("addOrderPage.html")
    return HttpResponse(template.render({'tables': tables, 'food': food, 'drinks': drinks}))


@user_passes_test(waiterCheck, login_url='./')
@csrf_exempt
def saveOrder(request):
    tableNumber = request.POST.get('tableNo')
    orderedFood = request.POST.get('foods')
    orderedDrinks = request.POST.get('drinks')
    print(tableNumber)
    orderedFood = orderedFood.strip()
    orderedDrinks = orderedDrinks.strip()
    food = orderedFood.split(' ')
    drinks = orderedDrinks.split(' ')
    e = Waiter.objects.get(email=request.user.username)
    em = []
    em.append(e)
    rest = e.restaurant
    t = RestaurantTable.objects.get(tableNo=tableNumber, restaurant=rest)
    order = Order.objects.create(table=t, paid=False)
    order.save()
    foodList = []
    foodDict = {}
    for i in food:
        f = Food.objects.get(id=i)
        foodDict[f] = 0
    for i in food:
        f = Food.objects.get(id=i)
        foodDict[f] += 1
    for key in foodDict:
        of = OrderedFood.objects.create(food=key, amount=foodDict[key])
        of.save()
        foodList.append(of)
    drinkList = []
    drinkDict = {}
    for i in drinks:
        d = Beaverage.objects.get(id=i)
        drinkDict[d] = 0
    for j in drinks:
        d = Beaverage.objects.get(id=j)
        drinkDict[d] += 1
    for key in drinkDict:
        od = OrderedDrink.objects.create(beaverage=key, amount=drinkDict[key])
        od.save()
        drinkList.append(od)
    order.ordereddrinks = drinkList
    order.orderedfoods = foodList
    order.employees = em
    order.save()
    orders = Order.objects.filter(employees=e)
    template = loader.get_template("waiterHomePage.html")
    user = request.user.username
    return HttpResponse(template.render({'user': user, 'order': orders}))



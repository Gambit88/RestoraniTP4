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
from restorani.models import TableHelp
from restorani.models import Schedule
from restorani.models import Notification
import datetime
import json
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

@login_required(redirect_field_name='IndexPage')
@user_passes_test(waiterCheck, login_url='./')
def waiterPage(request):
    if (request.user.last_name == "False"):
        user = request.user.username
        waiter = Waiter.objects.get(email=request.user.username)
        restaurant = waiter.restaurant
        orders = Order.objects.all()
        temp = []
        for i in orders:
            if restaurant == i.table.restaurant:
                temp.append(i)
        foodNotifications = Notification.objects.filter(type = "food")
        drinkNotifications = Notification.objects.filter(type = "drink")
        tables = RestaurantTable.objects.filter(restaurant=restaurant)
        tlist = []
        for i in range(restaurant.sizeX):
            for j in range(restaurant.sizeY):
                test = True
                # za stolove koji postoje
                if tables is not None:
                    for table in tables:
                        if i == table.posX and j == table.posY:
                            tableH = TableHelp()
                            tableH.num = table.tableNo
                            tableH.segment = table.segment.name
                            tlist.append(tableH)
                            test = False
                if test:
                    tableH = TableHelp()
                    tableH.num = ""
                    tableH.segment = ""
                    tlist.append(tableH)
        template = loader.get_template("waiterHomePage.html")
        schedule = Schedule.objects.filter(employee = waiter, date__gte = datetime.date.today())
        timeTemp = str(datetime.datetime.now().time()).split(':')
        time = timeTemp[0] + ':' + timeTemp[1]
        print(time)
        if time >= '08:00' and time <= '15:59':
            shift = 1
        if time >= '16:00' and time <= '23:59':
            shift = 2
        if time >= '00:00' and time <= '07:59':
            shift = 3
        segment = ""
        for i in schedule:
            if i.shift == shift:
                segment = i.segment
        listI = list(range(0, restaurant.sizeX))
        listJ = list(range(0,restaurant.sizeY))
        s = Schedule.objects.all()
        sc = []
        for i in s:
            if i.employee.restaurant == restaurant and i.employee.user.first_name == "WAITER":
               sc.append(i)
        shift1 = []
        shift2 = []
        shift3 = []
        for i in sc:
            if i.shift == 1:
                shift1.append(i)
            if i.shift == 2:
                shift2.append(i)
            if i.shift == 3:
                shift3.append(i)
        today = datetime.date.today()
        calendar1 = []
        calendar1.append(today)
        for i in range(1,5):
            today = today + datetime.timedelta(days=1)
            calendar1.append(today)
        calendar = []
        for i in calendar1:
            g = str(i)
            calendar.append(g)
        for i in shift1:
            i.date = str(i.date).split(' ')[0]
            i.save()
        for i in shift2:
            i.date = str(i.date).split(' ')[0]
            i.save()
        for i in shift3:
            i.date = str(i.date).split(' ')[0]
            i.save()
        return HttpResponse(template.render({'user': user, 'order': temp, 'tables':tlist, 'segment': segment,'listI':listI,'listJ':listJ,'foodNotifications':foodNotifications,'drinkNotifications':drinkNotifications,"calendar":calendar,'shift1': shift1,'shift2': shift2,'shift3': shift3}))
    else:
        template = loader.get_template("static/firstLoginPasswordChange.html")
        return HttpResponse(template.render())

@login_required(redirect_field_name='IndexPage')
@user_passes_test(waiterCheck, login_url='./')
def waiterProfile(request):
    waiter = Waiter.objects.get(email=request.user.username)
    link = "./waiterHomePage"
    template = loader.get_template("waiterProfile.html")
    return HttpResponse(template.render({'waiter': waiter, 'back': link}))

@login_required(redirect_field_name='IndexPage')
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

@login_required(redirect_field_name='IndexPage')
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

@login_required(redirect_field_name='IndexPage')
@user_passes_test(waiterCheck, login_url='./')
@csrf_exempt
def addOrder(request):  ##### IZBRISATI TESTIRANJE
    # waiter = request.user.employee
    waiter = Waiter.objects.get(email=request.user.username)
    restaurant = request.user.employee.restaurant
    tables = RestaurantTable.objects.filter(restaurant=restaurant)
    food = Food.objects.filter(restaurant=restaurant)
    drinks = Beaverage.objects.filter(restaurant=restaurant)
    template = loader.get_template("addOrder.html")
    return HttpResponse(template.render({'tables': tables, 'food': food, 'drinks': drinks}))

@login_required(redirect_field_name='IndexPage')
@user_passes_test(waiterCheck, login_url='./')
@csrf_exempt
def saveOrder(request):
    tableNumber = request.POST.get('tableNo')
    orderedFood = request.POST.get('foods')
    orderedDrinks = request.POST.get('drinks')
    orderedFood = orderedFood.strip()
    orderedDrinks = orderedDrinks.strip()
    food = []
    if orderedFood != '':
        food = orderedFood.split(' ')
    drinks = []
    if orderedDrinks != '':
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
    return redirect("waiterHomePage")
@login_required(redirect_field_name='IndexPage')
@user_passes_test(waiterCheck, login_url='./')
@csrf_exempt
def editOrder(request):
	order_id = request.POST.get('orderID')
	order = Order.objects.get(id = order_id)
	waiter = Waiter.objects.get(email=request.user.username)
	restaurant = request.user.employee.restaurant
	tables = RestaurantTable.objects.filter(restaurant=restaurant)
	template = loader.get_template("editOrder.html")
	return HttpResponse(template.render({'order': order}))
@login_required(redirect_field_name='IndexPage')
@user_passes_test(waiterCheck, login_url='./')
@csrf_exempt
def createBill(request):
	orderID = request.POST.get('orderID')
	order = Order.objects.get(id = orderID)
	total = 0
	foodTotal = 0
	drinkTotal = 0
	for i in order.orderedfoods.all():
		foodTotal += i.food.price * i.amount
	for i in order.ordereddrinks.all():
		drinkTotal += i.beaverage.price * i.amount
	total = foodTotal + drinkTotal
	template = loader.get_template('bill.html')
	return HttpResponse(template.render({'order':order,'total':total}))
@login_required(redirect_field_name='IndexPage')
@user_passes_test(waiterCheck, login_url='./')
@csrf_exempt
def payOrder(request):
    orderID = request.POST.get('orderID')
    order = Order.objects.get(id=orderID)
    order.paid = True
    order.save()
    user = request.user.username
    waiter = Waiter.objects.get(email=request.user.username)
    orders = Order.objects.filter(employees=waiter)
    return redirect("waiterHomePage")
@login_required(redirect_field_name='IndexPage')
@user_passes_test(waiterCheck, login_url='./')
@csrf_exempt
def addFood(request):
    order_id = request.POST.get('orderID')
    order = Order.objects.get(id = order_id)
    rest = ""
    for i in order.employees.all():
        rest = i.restaurant
    food = Food.objects.filter(restaurant=rest)
    template = loader.get_template("addFood.html")
    return HttpResponse(template.render({'order':order, 'food': food}))
@login_required(redirect_field_name='IndexPage')
@user_passes_test(waiterCheck, login_url='./')
@csrf_exempt
def addDrink(request):
    order_id = request.POST.get('orderID')
    order = Order.objects.get(id = order_id)
    rest = ""
    for i in order.employees.all():
        rest = i.restaurant
    drinks = Beaverage.objects.filter(restaurant=rest)
    template = loader.get_template("addDrink.html")
    return HttpResponse(template.render({'order': order, 'drinks': drinks}))
@login_required(redirect_field_name='IndexPage')
@user_passes_test(waiterCheck, login_url='./')
@csrf_exempt
def saveFoods(request):
    orderedFood = request.POST.get('foods')
    orderedFood = orderedFood.strip()
    order_id = request.POST.get('orderID')
    order = Order.objects.get(id=order_id)
    food = orderedFood.split(' ')
    foodListTmp = order.orderedfoods.all()
    foodDict = {}
    foodList = []
    for i in foodListTmp:
        foodList.append(i)
    for i in foodList:
        if i.food not in foodDict:
            foodDict[i.food] = i.amount
    for i in food:
        f = Food.objects.get(id=i)
        if f in foodDict:
            foodDict[f] += 1
        else:
            foodDict[f] = 1
    for key in foodDict:
        f = True
        for i in foodList:
            if key == i.food:
                f = False
                i.amount = foodDict[key]
                i.save()
        if f:
            of = OrderedFood.objects.create(food=key, amount=foodDict[key])
            of.save()
            foodList.append(of)
    order.orderedfoods = list()
    order.orderedfoods = foodList
    order.save()
    template = loader.get_template("editOrder.html")
    return HttpResponse(template.render({'order': order}))
@login_required(redirect_field_name='IndexPage')
@user_passes_test(waiterCheck, login_url='./')
@csrf_exempt
def saveDrinks(request):
    orderedDrinks = request.POST.get('drinks')
    orderedDrinks = orderedDrinks.strip()
    order_id = request.POST.get('orderID')
    order = Order.objects.get(id=order_id)
    drinks = orderedDrinks.split(' ')
    drinkListTmp = order.ordereddrinks.all()
    drinkDict = {}
    drinkList = []
    for i in drinkListTmp:
        drinkList.append(i)
    for i in drinkList:
        if i.beaverage not in drinkDict:
            drinkDict[i.beaverage] = i.amount
    for j in drinks:
        b = Beaverage.objects.get(id=j)
        if b in drinkDict:
            drinkDict[b] += 1
        else:
            drinkDict[b] = 1
    for key in drinkDict:
        f = True
        for i in drinkList:
            if key == i.beaverage:
                f = False
                i.amount = drinkDict[key]
                i.save()
        if f:
            od = OrderedDrink.objects.create(beaverage=key, amount=drinkDict[key])
            od.save()
            drinkList.append(od)
    order.ordereddrinks = list()
    order.ordereddrinks = drinkList
    order.save()
    template = loader.get_template("editOrder.html")
    return HttpResponse(template.render({'order': order}))
@login_required(redirect_field_name='IndexPage')
@user_passes_test(waiterCheck, login_url='./')
@csrf_exempt
def removeFood(request):
    orderID = request.POST.get('orderID')
    foodID = request.POST.get('foodID')
    f = Food.objects.get(id = foodID)
    order = Order.objects.get(id = orderID)
    foodTemp = order.orderedfoods.all()
    food = []
    for i in foodTemp:
        if i.food != f:
            food.append(i)
        else:
            if i.amount > 1:
                i.amount -= 1
                i.save()
                food.append(i)
    order.orderedfoods = list()
    order.orderedfoods = food
    order.save()
    template = loader.get_template("editOrder.html")
    return HttpResponse(template.render({'order': order}))
@login_required(redirect_field_name='IndexPage')
@user_passes_test(waiterCheck, login_url='./')
@csrf_exempt
def removeDrink(request):
    orderID = request.POST.get('orderID')
    drinkID = request.POST.get('drinkID')
    order = Order.objects.get(id=orderID)
    b = Beaverage.objects.get(id=drinkID)
    drinkTemp = order.ordereddrinks.all()
    drink = []
    for i in drinkTemp:
        if i.beaverage != b:
            drink.append(i)
        else:
            if i.amount > 1:
                i.amount -= 1
                i.save()
                drink.append(i)
    order.ordereddrinks = list()
    order.ordereddrinks= drink
    order.save()
    template = loader.get_template("editOrder.html")
    return HttpResponse(template.render({'order': order}))
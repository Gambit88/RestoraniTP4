from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Restaurant(models.Model):  # done
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    address = models.CharField(max_length=50, null=True)
    sizeX = models.IntegerField()
    sizeY = models.IntegerField()
    long = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)


class Beaverage(models.Model):  # done
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class Employee(models.Model):  #
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=35)
    email = models.EmailField(max_length=250)
    restaurant = models.ForeignKey(Restaurant)
    firstLogin = models.BooleanField()
    shoeSize = models.CharField(max_length=20)
    size = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


class Food(models.Model):  # done
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    restaurant = models.ForeignKey(Restaurant)


class Segment(models.Model):  # done
    name = models.CharField(max_length=30)
    restaurant = models.ForeignKey(Restaurant)


class RestaurantTable(models.Model):  # done
    tableNo = models.IntegerField(null=True)
    segment = models.ForeignKey(Segment)
    restaurant = models.ForeignKey(Restaurant)
    chairNo = models.IntegerField()
    posX = models.IntegerField()
    posY = models.IntegerField()


class Reservation(models.Model):  # done
    restaurantTables = models.ManyToManyField(RestaurantTable)
    date = models.DateTimeField()
    duration = models.IntegerField()
    complete = models.BooleanField()
    rated = models.BooleanField(default=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)

class Guest(models.Model):  # done
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    reservations = models.ManyToManyField(Reservation)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=35)
    email = models.EmailField(max_length=250)
    activated = models.BooleanField()
    address = models.CharField(max_length=250)
    long = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    friends = models.ManyToManyField("Guest")
	
class InviteList(models.Model):
	reservation = models.OneToOneField(Reservation, null=True)
	guests = models.ManyToManyField(Guest)

class Post(models.Model):  # done
    content = models.CharField(max_length=500, null=True)
    expiration_date = models.DateTimeField()
    restaurant = models.ForeignKey(Restaurant)


class Supplier(models.Model):  # done
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=35)
    email = models.EmailField(max_length=250)
    posts = models.ManyToManyField(Post)


class Offer(models.Model):  # done
    supplier = models.ForeignKey(Supplier)
    price = models.CharField(max_length=30, null=True)
    post = models.ForeignKey(Post)
    acepted = models.BooleanField()


class OrderedFood(models.Model):
    food = models.ForeignKey(Food)
    amount = models.IntegerField()

class OrderedDrink(models.Model):
    beaverage = models.ForeignKey(Beaverage)
    amount = models.IntegerField()

class Order(models.Model):  # done
    ordereddrinks = models.ManyToManyField(OrderedDrink)
    table = models.ForeignKey(RestaurantTable)
    orderedfoods = models.ManyToManyField(OrderedFood)
    employees = models.ManyToManyField(Employee)
    paid = models.BooleanField()
    time = models.CharField(max_length=100, default="Now")


class RatingFood(models.Model):  # done
    rating = models.IntegerField()
    food = models.ForeignKey(Food, null=True)


class RatingRestaurant(models.Model):  # done
    rating = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant)
    guest = models.ForeignKey(Guest, null=True)


class RatingServices(models.Model):  # done
    rating = models.IntegerField()
    employee = models.ForeignKey(Employee, null=True)


class RestaurantManager(models.Model):  # done
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=35)
    email = models.EmailField(max_length=250)
    restaurant = models.ForeignKey(Restaurant)


class Schedule(models.Model):  # done
    segment = models.ForeignKey(Segment, null = True)
    employee = models.ForeignKey(Employee)
    shift = models.IntegerField()
    date = models.DateTimeField()


class SystemManager(models.Model):  # done
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=35)
    email = models.EmailField(max_length=250)


class Bartender(Employee):  # done
    pass


class Waiter(Employee):  # done
    pass


class Cook(Employee):  # done
    kind = models.CharField(max_length=80)


class TableHelp():
    posX = 0
    posY = 0
    status = False
    num = ""
    chairs = 0
    id = None
    segment = ""

class Notification(models.Model):
    order = models.ForeignKey(Order)
    message = models.CharField(max_length=50)
    type = models.CharField(max_length=10, null = True)
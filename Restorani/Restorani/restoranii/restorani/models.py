from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Restaurant(models.Model):#done
	name = models.CharField(max_length = 50)
	type = models.CharField(max_length = 50)
	sizeX = models.IntegerField()
	sizeY = models.IntegerField()

class Beaverage(models.Model):#done
	name = models.CharField(max_length = 50)
	description = models.CharField(max_length=100)
	price = models.FloatField(default=0.0)
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
	
class Employee(models.Model):#
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length = 30)
	surname = models.CharField(max_length = 35)
	email = models.EmailField(max_length = 250)
	password = models.CharField(max_length = 40)
	restaurant = models.ForeignKey(Restaurant)
	firstLogin = models.BooleanField()
	shoeSize = models.CharField(max_length = 20)
	size = models.CharField(max_length = 20)

class Food(models.Model):#done
	name = models.CharField(max_length = 50)
	description = models.CharField(max_length = 200)
	price = models.FloatField()
	restaurant = models.ForeignKey(Restaurant)
	
class Segment(models.Model):#done
	name = models.CharField(max_length = 30)
	restaurant = models.ForeignKey(Restaurant)

class RestaurantTable(models.Model):#done
	segment = models.ForeignKey(Segment)
	restaurant = models.ForeignKey(Restaurant)
	chairNo = models.IntegerField()
	posX = models.IntegerField()
	posY = models.IntegerField()

class Reservation(models.Model):#done
	restaurantTables = models.ManyToManyField(RestaurantTable)
	date = models.DateTimeField()
	duration = models.IntegerField()
	complete = models.BooleanField()

class Guest(models.Model):#done
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	reservations = models.ManyToManyField(Reservation)
	name = models.CharField(max_length = 30)
	surname = models.CharField(max_length = 35)
	email = models.EmailField(max_length = 250)
	password = models.CharField(max_length = 40)
	activated = models.BooleanField()
	address = models.CharField(max_length = 250)
	reservations = models.ManyToManyField(Reservation)
	friends = models.ManyToManyField("Guest")
	
class Post(models.Model):#done
	expiration_date = models.DateTimeField()
	restaurant = models.ForeignKey(Restaurant)
	
class Supplier(models.Model):#done
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length = 30)
	surname = models.CharField(max_length = 35)
	email = models.EmailField(max_length = 250)
	password = models.CharField(max_length = 40)
	posts = models.ManyToManyField(Post)

class Offer(models.Model):#done
	supplier = models.ForeignKey(Supplier)
	post = models.ForeignKey(Post)
	acepted = models.BooleanField()
	
class Order(models.Model):#done
	beaverages = models.ManyToManyField(Beaverage)
	table = models.ForeignKey(RestaurantTable)
	foods = models.ForeignKey(Food)
	employees = models.ManyToManyField(Employee)
	paid = models.BooleanField()
	
class RatingFood(models.Model):#done
	rating = models.IntegerField()
	foods = models.ManyToManyField(Food)
	
class RatingRestaurant(models.Model):#done
	rating = models.IntegerField()
	restaurant = models.ForeignKey(Restaurant)
	
class RatingServices(models.Model):#done
	rating = models.IntegerField()
	employees = models.ManyToManyField(Employee)
	

	
class RestaurantManager(models.Model):#done
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length = 30)
	surname = models.CharField(max_length = 35)
	email = models.EmailField(max_length = 250)
	password = models.CharField(max_length = 40)
	restaurant = models.ForeignKey(Restaurant)
	

	
class Schedule(models.Model):#done
	segment = models.ForeignKey(Segment)
	employee = models.ForeignKey(Employee)
	shift = models.IntegerField()
	date = models.DateTimeField()
	
class SystemManager(models.Model):#done
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length = 30)
	surname = models.CharField(max_length = 35)
	email = models.EmailField(max_length = 250)
	password = models.CharField(max_length = 40)
	
class Bartender(Employee):#done
	pass

class Waiter(Employee):#done
	pass

class Cook(Employee):#done
	kind = models.CharField(max_length=80)
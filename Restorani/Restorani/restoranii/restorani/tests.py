from django.test import TestCase
from restorani.models import Guest
from restorani.models import Restaurant
from restorani.models import RestaurantManager
from restorani.models import Employee
from restorani.models import Waiter
from restorani.models import Bartender
from restorani.models import Cook
from django.contrib.auth.models import User

# Create your tests here.
class UserTestCase(TestCase):
	def setUp(self):
		user = User.objects.create_user(username = "testRestTP4@gmail.com", password = 'password', first_name="GUEST")
		Guest.objects.create(user=user, name='name', surname='surname', address='address', email= "testRestTP4@gmail.com",activated=False)
		restaurant = Restaurant.objects.create(name="name", type="type", address="address", sizeX=150, sizeY=200)
		user_manager = User.objects.create_user(username="mirjana@gmail.com", password='password', first_name="MANAGER")
		manager = RestaurantManager.objects.create(name="manager", surname="lastname", email="mirjana@gmail.com",
												   user=user_manager, restaurant=restaurant)
		user_waiter = User.objects.create_user(username="waiter@gmail.com", password='password', first_name="WAITER")
		waiter = Waiter.objects.create(name="name",
									   surname="lastname", email="waiter@gmail.com",
									   shoeSize=36, size="Woman S",
									   user=user_waiter,
									   restaurant=restaurant, firstLogin=False)
		user_bartender = User.objects.create_user(username="bartender@gmail.com", password='password', first_name="BARTENDER")
		bartender = Bartender.objects.create(name="name",
									   surname="lastname", email="bartender@gmail.com",
									   shoeSize=36, size="Woman S",
									   user=user_bartender,
									   restaurant=restaurant, firstLogin=False)
		user_cook = User.objects.create_user(username="cook@gmail.com", password='password', first_name="COOK")
		cook = Cook.objects.create(name="name", kind = "kind",
									   surname="lastname", email="cook@gmail.com",
									   shoeSize=36, size="Woman S",
									   user=user_cook,
									   restaurant=restaurant, firstLogin=False)
	def test_user(self):
		user = User.objects.get(username="testRestTP4@gmail.com")
		self.assertEqual(user.first_name,"GUEST")
	def test_guest(self):
		guest = Guest.objects.get(email = "testRestTP4@gmail.com")
		self.assertEqual(guest.user.username, "testRestTP4@gmail.com")
		self.assertEqual(guest.user.first_name, "GUEST")
	def test_equal(self):
		user = User.objects.get(username="testRestTP4@gmail.com")
		guest = Guest.objects.get(email = "testRestTP4@gmail.com")
		self.assertEqual(guest.user.username, user.username)

	def test_manager_restaurant(self):
		manager = RestaurantManager.objects.get(email="mirjana@gmail.com")
		user_manager = User.objects.get(username="mirjana@gmail.com")
		self.assertEqual(manager.user.first_name, "MANAGER")

	def test_waiter(self):
		self.assertIsNotNone(Employee.objects.get(email = "waiter@gmail.com"), msg=None)

	def test_bartender(self):
		self.assertIsNotNone(Employee.objects.get(email = "bartender@gmail.com"), msg=None)

	def test_cook(self):
		self.assertIsNotNone(Employee.objects.get(email="cook@gmail.com"), msg=None)
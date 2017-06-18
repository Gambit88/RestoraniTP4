from django.test import TestCase
from restorani.models import Guest
from restorani.models import Restaurant
from restorani.models import  RestaurantManager
from django.contrib.auth.models import User

# Create your tests here.
class UserTestCase(TestCase):
	def setUp(self):
		user = User.objects.create_user(username = "testRestTP4@gmail.com", password = 'password', first_name="GUEST")
		Guest.objects.create(user=user, name='name', surname='surname', address='address', email= "testRestTP4@gmail.com",activated=False)
		restaurant = Restaurant.objects.create(name="name", type="type", address="address", sizeX=150, sizeY=200)
		manager = RestaurantManager.objects.cerate(name="manager", surname="lastname", email="testRestTP4@gmail.com",
												   user=user, restaurant=restaurant)
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
		manager = RestaurantManager.objects.get(email="testRestTP4@gmail.com")
		user = User.objects.get(username="testRestTP4@gmail.com")
		self.assertEqual(manager.user.first_name, "MANAGER")
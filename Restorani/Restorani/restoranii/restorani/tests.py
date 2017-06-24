from django.test import TestCase, Client
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
		Guest.objects.create(user=user, name='name', surname='surname', address='address', email= "testRestTP4@gmail.com",activated=False, long=1, lat=1)
		user2 = User.objects.create_user(username = "testRestTP42@gmail.com", password = 'password', first_name="GUEST")
		Guest.objects.create(user=user2, name='name', surname='surname', address='address', email= "testRestTP42@gmail.com",activated=True, long=1, lat=1)
	
		restaurant = Restaurant.objects.create(name="name", type="type", address="address", sizeX=10, sizeY=10, long=0, lat=0)
		
		user_manager = User.objects.create_user(username="mirjana@gmail.com", password='password', first_name="MANAGER")
		manager = RestaurantManager.objects.create(name="manager", surname="lastname", email="mirjana@gmail.com",user=user_manager, restaurant=restaurant)
		
		user_waiter = User.objects.create_user(username="waiter@gmail.com", password='password', first_name="WAITER")
		
		waiter = Waiter.objects.create(name="name",surname="lastname", email="waiter@gmail.com",shoeSize=36, size="Woman S",user=user_waiter,restaurant=restaurant, firstLogin=False)
		
		user_bartender = User.objects.create_user(username="bartender@gmail.com", password='password', first_name="BARTENDER")
		bartender = Bartender.objects.create(name="name",surname="lastname", email="bartender@gmail.com",shoeSize=36, size="Woman S",user=user_bartender,restaurant=restaurant, firstLogin=False)
		
		user_cook = User.objects.create_user(username="cook@gmail.com", password='password', first_name="COOK")
		cook = Cook.objects.create(name="name", kind = "kind",surname="lastname", email="cook@gmail.com",shoeSize=36, size="Woman S",user=user_cook,restaurant=restaurant, firstLogin=False)

	#testovi
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
		self.assertEqual(guest.user, user)
	#redirect testovi
	#neaktivni user
	def test_red_test(self):
		c = Client()
		self.assertTrue(c.login(username = "testRestTP4@gmail.com", password = 'password'))
		response = c.get('/restoranii/')
		self.assertRedirects(response,'/restoranii/guestHomePage', status_code=302,target_status_code=302, fetch_redirect_response=True)
	#aktivan guest
	def test_red_test(self):
		c = Client()
		self.assertTrue(c.login(username = "testRestTP42@gmail.com", password = 'password'))
		response = c.get('/restoranii/')
		self.assertRedirects(response,'/restoranii/guestHomePage', status_code=302,target_status_code=200, fetch_redirect_response=True)
	#menadzer restorana
	def test_red_test2(self):
		c = Client()
		self.assertTrue(c.login(username="mirjana@gmail.com", password='password'))
		response = c.get('/restoranii/')
		self.assertRedirects(response,'/restoranii/rmHomePage', status_code=302,target_status_code=200, fetch_redirect_response=True)
	#konobar
	def test_red_test3(self):
		c = Client()
		c.login(username="waiter@gmail.com", password='password')
		response = c.get('/restoranii/')
		self.assertRedirects(response,'/restoranii/waiterHomePage', status_code=302,target_status_code=200, fetch_redirect_response=True)
	#kuvar
	def test_red_test4(self):
		c = Client()
		c.login(username="cook@gmail.com", password='password')
		response = c.get('/restoranii/')
		self.assertRedirects(response,'/restoranii/cookHomePage', status_code=302,target_status_code=200, fetch_redirect_response=True)
	#login testovi
	#uloguje se
	def test_login_test(self):
		c = Client()
		response = c.post('/restoranii/login',{'email':'testRestTP4@gmail.com','password':'password'})
		self.assertRedirects(response,'/restoranii/', status_code=302,target_status_code=302, fetch_redirect_response=True)
	#pogresna sifra
	def test_login_test2(self):
		c = Client()
		response = c.post('/restoranii/login',{'email':"testRestTP4@gmail.com","password":'password1'})
		self.assertEqual(response.status_code,200)
	#logout testovi
	def test_logout(self):
		c = Client()
		c.login(username="waiter@gmail.com", password='password')
		response = c.get('/restoranii/logout')
		self.assertRedirects(response,'/restoranii/', status_code=302,target_status_code=200, fetch_redirect_response=True)
		
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
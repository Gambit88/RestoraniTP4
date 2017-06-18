from django.test import TestCase
from restorani.models import Guest
from django.contrib.auth.models import User

# Create your tests here.
class UserTestCase(TestCase):
	def setUp(self):
		user = User.objects.create_user(username = "testRestTP4@gmail.com", password = 'password', first_name="GUEST")
		Guest.objects.create(user=user, name='name', surname='surname', address='address', email= "testRestTP4@gmail.com",activated=False)
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

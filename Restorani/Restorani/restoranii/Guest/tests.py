from django.test import TestCase, Client
from django.contrib.auth.models import User
from restorani.models import Guest

# Create your tests here.
class GuestTestCase(TestCase):
	def setUp(self):
		user = User.objects.create_user(username = "testRestTP41g@gmail.com", password = 'password', first_name="GUEST")
		self.guest1 = Guest.objects.create(user=user, name='name', surname='surname', address='address', email= "testRestTP41g@gmail.com",activated=False, long=1, lat=1)
		user2 = User.objects.create_user(username = "testRestTP42g@gmail.com", password = 'password', first_name="GUEST")
		self.guest2 = Guest.objects.create(user=user2, name='name', surname='surname', address='address', email= "testRestTP42g@gmail.com",activated=True, long=1, lat=1)
		user3 = User.objects.create_user(username = "testRestTP43g@gmail.com", password = 'password', first_name="GUEST")
		self.guest3 = Guest.objects.create(user=user3, name='name', surname='surname', address='address', email= "testRestTP43g@gmail.com",activated=True, long=1, lat=1)
	#test aktivacije racuna
	def test_activate(self):
		c = Client()
		self.assertTrue(self.guest1.activated==False)
		c.get('/restoranii/activate',{'id':self.guest1.id})
		g = Guest.objects.get(id=self.guest1.id)
		self.assertTrue(g.activated==True)
		
	#registracija
	def test_regGuest(self):
		c = Client()
		response = c.post('/restoranii/guestRegister',{'email':'djordjeilic55@gmail.com','password':'password','passwordR':'password','name':'n','surname':'sn','address':'Srbija Valjevo Uzicka 1'})
		g = Guest.objects.get(email='djordjeilic55@gmail.com')
		self.assertTrue(g.activated==False)
		self.assertTrue(g.email=='djordjeilic55@gmail.com')
	
	def test_addAndRemoveFriend(self):
		c = Client()
		c.login(username='testRestTP41g@gmail.com',password = 'password')
		g = Guest.objects.get(email='testRestTP41g@gmail.com')
		self.assertFalse(g.friends.filter(pk=self.guest3.id))
		c.post('/restoranii/Friends/',{'type':'add','email':'testRestTP43g@gmail.com'})
		g = Guest.objects.get(email='testRestTP41g@gmail.com')
		self.assertTrue(g.friends.filter(pk=self.guest3.id))
		self.assertFalse(g.friends.filter(pk=self.guest2.id))
		c.post('/restoranii/Friends/',{'type':'del','identity':self.guest3.id})
		g = Guest.objects.get(email='testRestTP41g@gmail.com')
		self.assertFalse(g.friends.filter(pk=self.guest3.id))
	
	def test_editProfile(self):
		c = Client()
		c.login(username='testRestTP41g@gmail.com',password = 'password')
		#ime
		g = Guest.objects.get(email='testRestTP41g@gmail.com')
		self.assertEquals(g.name,"name")
		c.post('/restoranii/EditProfileGuest/',{'type':'n','name':'new'})
		g = Guest.objects.get(email='testRestTP41g@gmail.com')
		self.assertEquals(g.name,"new")
		#prezime
		g = Guest.objects.get(email='testRestTP41g@gmail.com')
		self.assertEquals(g.surname,"surname")
		c.post('/restoranii/EditProfileGuest/',{'type':'s','surname':'newS'})
		g = Guest.objects.get(email='testRestTP41g@gmail.com')
		self.assertEquals(g.surname,"newS")
		#adresa
		g = Guest.objects.get(email='testRestTP41g@gmail.com')
		self.assertEquals(g.address,"address")
		c.post('/restoranii/EditProfileGuest/',{'type':'a','address':'Srbija Beograd'})
		g = Guest.objects.get(email='testRestTP41g@gmail.com')
		self.assertEquals(g.address,"Srbija Beograd")
		#sifra
		c.logout()
		self.assertTrue(c.login(username='testRestTP41g@gmail.com',password = 'password'))
		c.post('/restoranii/EditProfileGuest/',{'type':'p','opass':'password', 'pass':'newPass', 'rpass':'newPass'})
		self.assertFalse(c.login(username='testRestTP41g@gmail.com',password = 'password'))
		self.assertTrue(c.login(username='testRestTP41g@gmail.com',password = 'newPass'))
		
		
	
		
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from .managers import MyUserManager
from rest_framework.authtoken.models import Token

class MyUser(AbstractBaseUser,PermissionsMixin):
	username = models.CharField(max_length = 16, unique = True)
	email = models.EmailField(_('email address'), unique = True)
	first_name = models.CharField(max_length = 20)
	last_name = models.CharField(max_length = 20)
	phone_no = models.IntegerField()
	address = models.TextField(max_length =100)
	is_verified = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email','phone_no']
	
	objects = MyUserManager()
	
	def __str__(self):
		return self.username

	@property
	def token(self):
		token = Token.objects.get(user=MyUser.objects.get(self.id))
		return token


class Product(models.Model):
	STOCK = (
	('In Stock', 'In Stock'),
	('Out of stock' , 'Out of stock'),
	)
	
	STARS =(
	('1','1 Star'),
	('2','2 Stars'),
	('3','3 Stars'),
	('4','4 Stars'),
	('5','5 Stars'),
	)
	
	name = models.CharField(max_length = 100)
	price = models.FloatField()
	description = models.CharField(max_length = 100)
	stock_status = models.CharField(max_length = 100, choices = STOCK)
	rating = models.CharField(max_length = 100, choices = STARS)
	date_created = models.DateTimeField(auto_now_add = True)
	
	def __str__(self):
		return self.name
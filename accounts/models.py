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
	address = models.TextField(max_length =100, blank = True)
	is_active = models.BooleanField(default=False)
	is_seller = models.BooleanField(default = False)
	is_staff = models.BooleanField(default=False)
	provider = models.CharField(max_length = 20,default = 'email')
	
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email','phone_no']
	
	objects = MyUserManager()
	
	def __str__(self):
		return self.username

	@property
	def token(self):
		token = Token.objects.get(user=MyUser.objects.get(self.id))
		return token
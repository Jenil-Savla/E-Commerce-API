from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class MyUserManager(BaseUserManager):
	def create_user(self,username, email,password=None,**extra_fields):
		if not username:
			raise ValueError('Users must have an username')
		user = self.model(username=username, email=self.normalize_email(email),**extra_fields)
		if not password:
			password = 'user1234'
		user.set_password(password)
		user.save()
		return user
		
	def create_superuser(self,username, email,phone_no,password=None,**extra_fields):
		extra_fields.setdefault('is_seller',True)
		extra_fields.setdefault('is_active',True)
		extra_fields.setdefault('is_staff',True)
		extra_fields.setdefault('is_superuser',True)
		user = self.create_user(username,email, phone_no,password,**extra_fields)
		user.save()
		return user		
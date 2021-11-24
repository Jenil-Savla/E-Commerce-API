from rest_framework import serializers
import environ
from .models import MyUser
from .register import register_social_user
from rest_framework.exceptions import AuthenticationFailed

env = environ.Env()
environ.Env.read_env()

class RegisterSerializer(serializers.ModelSerializer):
	password=serializers.CharField(max_length=32,min_length=8,write_only = True)
	
	class Meta:
		model = MyUser
		fields = ['username','email','password','first_name','last_name','phone_no','address']
		
	def validate(self,attrs):
		username = attrs.get('username',' ')
		email = attrs.get('email',' ')
		if not username.isalnum():
			raise serializers.ValidationError('Username must be alphanumeric only')
		return attrs
		
	def create(self,validated_data):
		return MyUser.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
	password=serializers.CharField(max_length=32,min_length=8,write_only = True)
	
	class Meta:
		model = MyUser
		fields = ['username','password']

		
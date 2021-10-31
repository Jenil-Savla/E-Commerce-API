from rest_framework import serializers
import environ
from .models import MyUser
from .Utils import Google
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
		

class OAuthSerializer(serializers.Serializer):
	
	auth_token = serializers.CharField()

	def create_socialuser(username,email,phone_no, password):
		pass
	
	def validate_auth_token(self,auth_token):
		user_data = Google.validate(auth_token)
		try:
			user_data['sub']
		except:
			raise serializers.ValidationError('Token is invalid')
		
		if user_data['aud'] != env('CLIENT_ID'): #Client Id
			raise AuthenticationFailed('Credentials are Invalid')
		username = user_data['sub']
		email = user_data['email']
		first_name = user_data['name']
		return register_social_user(provider='google',username = username,email=email,name=first_name,phone_no = 123)
		
		#secret = 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
		
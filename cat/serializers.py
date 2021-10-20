from rest_framework import serializers
from .models import Product,MyUser

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


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'
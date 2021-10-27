from rest_framework import serializers
from .models import MyUser
#from .Utils import Google
#from .managers import MyUserManager

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
		
'''
class OAuthSerializer(serializers.Serializer):
	
	auth_token = serializers.CharField()
	
	def validate_auth_token(self,auth_token):
		user_data = Google.validate(auth_token)
		try:
			user_data['sub']
		except:
			raise serializers.ValidationError('Token is invalid')
		
		if user_data['aud'] != 655444446445-gjo2675tlflhrkla15rdldn1sa2qvrto.apps.googleusercontent.com: #Client Id
			raise AuthenticationFailed('Crednlentials are Invalid')
		username = user_data['sub']
		email = user_data['email']
		first_name = user_data['name']
		return MyUserManager.create_user(username = username,email=email,phone_no = 123, password = "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")
		
		#secret = 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
		'''
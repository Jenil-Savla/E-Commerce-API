from django.contrib.auth import authenticate,login
from django.shortcuts import redirect

from .models import MyUser
from .serializers import RegisterSerializer, LoginSerializer
from .Utils import Util

from rest_framework.generics import GenericAPIView
from rest_framework import mixins,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


class RegisterAPI(GenericAPIView):
	
	serializer_class = RegisterSerializer
	
	def post(self,request,*args,**kwargs):
		data = request.data
		serializer = self.serializer_class(data=data)
		serializer.is_valid(raise_exception = True)
		user = serializer.save()
		token = Token.objects.create(user=user)
		current_site = get_current_site(request).domain
		relative_link = reverse('email-verify')
		link = 'http://'+current_site+relative_link+'?token='+ token.key
		data = {'email_body': f'Use this link to get verified {link} ', 'subject':'Email Verification', 'to' : user.email}
		Util.send_email(data)
		
		return Response(serializer.data
		,status=status.HTTP_201_CREATED)


class LoginAPI(GenericAPIView):
	
	serializer_class = LoginSerializer
	
	def post(self,request,*args,**kwargs ):
		username = request.data.get('username',None)
		password = request.data.get('password',None)
		user1 = MyUser.objects.get(username = username)
		print(user1)
		user = authenticate(username = username, password = password)
		print(user)
		if user :
			login(request,user)
			serializer = self.serializer_class(user)
			token = Token.objects.get(user=user)
			return Response({'token' : token.key,'username' : user.username},status = status.HTTP_200_OK)
		return Response('Invalid Credentials',status = status.HTTP_404_NOT_FOUND)
		
class EmailVerify(GenericAPIView):
	def get(self,request):
		token = request.GET.get('token')
		user = MyUser.objects.get(auth_token = token)
		if not user.is_verified:
			user.is_verified = True
			user.save()
		return Response('Account Verified', status=status.HTTP_200_OK)
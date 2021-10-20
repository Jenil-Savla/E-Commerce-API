from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import redirect

from .models import Product,MyUser
from .serializers import ProductSerializer,RegisterSerializer, LoginSerializer
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
		link = 'http://'+current_site+relative_link+'?username='+user.username
		data = {'email_body': ' ', 'subject':'Email Verification', 'to' : user.email}
		#Util.send_email(data)
		
		return Response(serializer.data
		,status=status.HTTP_201_CREATED)


class LoginAPI(GenericAPIView):
	
	serializer_class = LoginSerializer
	
	def post(self,request,*args,**kwargs ):
		username = request.data.get('username',None)
		password = request.data.get('password',None)
		user = authenticate(username = username, password = password)
		if user :
			serializer = self.serializer_class(user)
			token = Token.objects.get(user=user)
			return Response({'token' : token.key,'username' : user.username},status = status.HTTP_200_OK)
		return Response('Invalid Credentials',status = status.HTTP_404_NOT_FOUND)
		
class EmailVerify(GenericAPIView):
	def get(self,request):
		username = request.GET.get('username')
		user = MyUser.objects.get(username = username)
		if not user.is_verified:
			user.is_verified = True
			user.save()
		return Response('Account Verified', status=status.HTTP_200_OK)

class Catalogue(mixins.ListModelMixin,GenericAPIView):
	
	serializer_class = ProductSerializer
	queryset = Product.objects.all()
	
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

class ProductCreate(mixins.CreateModelMixin, GenericAPIView):

    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()

    def post(self, request, *args, **kwargs):
       return self.create(request, *args, **kwargs)


class ProductRUD(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView
):

    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
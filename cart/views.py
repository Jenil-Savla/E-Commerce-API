from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from store.models import Product

from .models import Order,CartItem
from .serializers import OrderSerializer, CartItemSerializer

from rest_framework.response import Response

class CartView(GenericAPIView):
	permission_classes = [IsAuthenticated]

	def get(self, request, *args, **kwargs):
		user = request.user
		cart = Order.objects.filter(user = user,ordered = False).first()
		queryset = CartItem.objects.filter(cart=cart)
		serializer = CartItemSerializer(queryset,many = True)
		return Response(serializer.data, status = status.HTTP_200_OK)
		
	def post(self, request, *args, **kwargs):
		data = request.data
		user = request.user
		cart,_ = Order.objects.get_or_create(user = user, ordered = False)
		product = Product.objects.get(id=data.get('product'))
		price = product.price
		quantity = data.get('quantity')
		cart_items = CartItem(user=user,cart=cart,product=product, price = price,quantity=quantity)
		cart_items.save()
		return Response({'success':'Items added to your cart'}, status = status.HTTP_201_CREATED)
		
	def put(self, request, *args, **kwargs):
		data = request.data
		cart_item = CartItem.object.get(id = data.get('id'))
		quantity = data.get('quantity')
		cart_item.quantity = quantity
		cart_item.save()
		return Response({'success': 'Item Updated successfully'}, status = status.HTTP_200_OK)
		
		
	def delete(self, request, *args, **kwargs):
		user = request.user
		data = request.data
		
		cart_item = CartItem.objects.get(id = data.get('id'))
		cart_item.delete()
		
		cart = Cart.objects.filter(user = user,ordered = False).first()
		queryset = CartItems.objects.filter(cart=cart)
		serializer = CartItemSerializer(queryset,many = True)
		return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
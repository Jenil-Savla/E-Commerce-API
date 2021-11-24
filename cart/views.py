from django.shortcuts import render,redirect

import environ
from rest_framework.decorators import api_view
from . import Checksum
import requests
import json

env = environ.Env()
environ.Env.read_env()

from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from store.models import Product

from .models import Order,CartItem
from .serializers import CartItemSerializer

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
		cart.save()
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
		print(data.get('id'))
		cart_item = CartItem.objects.get(id = data.get('id'))
		cart_item.delete()
		
		cart = Order.objects.filter(user = user,ordered = False).first()
		queryset = CartItem.objects.filter(cart=cart)
		serializer = CartItemSerializer(queryset,many = True)
		return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
		
		
@api_view(['POST'])
def start_payment(request,pk):

    # we are saving an order instance
    order = Order.objects.get(id = pk)
    queryset = CartItem.objects.filter(cart=order).first()
    serializer = CartItemSerializer(queryset)
    # we have to send the param_dict to the frontend
    # these credentials will be passed to paytm order processor to verify the business account
    param_dict = {
        'MID': env('MERCHANTID'),
        'ORDER_ID': str(order.id)+'1',
        'TXN_AMOUNT': str(serializer.data['cart']['final_payment']),
        'CUST_ID': str(order.user.id),
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'http://127.0.0.1:8000/cart/handlepayment/',
        # this is the url of handlepayment function, paytm will send a POST request to the fuction associated with this CALLBACK_URL
    }

    ## create new checksum (unique hashed string) using our merchant key with every paytm payment
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, env('MERCHANTKEY'))
    # send the dictionary with all the credentials to the frontend
    return render(request,'paytm/checkout.html', context = param_dict)


@api_view(['POST'])
def handlepayment(request):
    checksum = ""
    # the request.POST is coming from paytm
    form = request.POST

    response_dict = {}
    order = None  # initialize the order varible with None

    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            # 'CHECKSUMHASH' is coming from paytm and we will assign it to checksum variable to verify our paymant
            checksum = form[i]

        if i == 'ORDERID':
            # we will get an order with id==ORDERID to turn isPaid=True when payment is successful
            order = Order.objects.get(id=form[i])

    # we will verify the payment using our merchant key and the checksum that we are getting from Paytm request.POST
    verify = Checksum.verify_checksum(response_dict, env('MERCHANTKEY'), checksum)

    if verify:
        if response_dict['RESPCODE'] == '01':
            # if the response code is 01 that means our transaction is successfull
            print('order successful')
            # after successfull payment we will make isPaid=True and will save the order
            order.ordered = True
            order.save()
            # we will render a template to display the payment status
            return render(request, 'paytm/paymentstatus.html', {'response': response_dict})
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
            return render(request, 'paytm/paymentstatus.html', {'response': response_dict})
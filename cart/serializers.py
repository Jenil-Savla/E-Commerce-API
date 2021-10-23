from rest_framework import serializers
from .models import Order,CartItem
from store.serializers import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
	final_payment = serializers.SerializerMethodField()
	class Meta:
		model = Order
		fields = '__all__'
		
	def get_final_payment(self,obj):
		final_payment = obj.final_payment
		cart_item = CartItem.objects.filter(cart= obj)
		for item in cart_item:
			final_payment += item.get_total_price()
		return final_payment
		
	
class CartItemSerializer(serializers.ModelSerializer):
	cart = OrderSerializer()
	product = ProductSerializer()
	class Meta:
		model = CartItem
		fields = '__all__'
	
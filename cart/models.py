from django.db import models
from accounts.models import MyUser
from store.models import Product

class Order(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    product = models.ManyToManyField('CartItem',blank= True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    final_payment = models.FloatField(default = 0)

    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    cart = models.ForeignKey(Order,on_delete = models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default = 0)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
    	return f"{self.quantity} of {self.product.name}"
    
    def get_total_price(self):
        return self.quantity * self.product.price
        

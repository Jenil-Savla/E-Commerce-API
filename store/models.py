from django.db import models
from accounts.models import MyUser
from django.utils.text import slugify

class Category(models.Model):
	category_name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length = 200, blank = True)
	
	class Meta:
	       verbose_name_plural = "Categories"
        
	def save(self,*args,**kwargs):
		self.slug = slugify(self.category_name)
		super(Category,self).save(*args,**kwargs)
		
	def __str__(self):
		return self.category_name
		

class Product(models.Model):
	STOCK = (
	('In Stock', 'In Stock'),
	('Out of stock' , 'Out of stock'),
	)
	
	STARS =(
	('1','1 Star'),
	('2','2 Stars'),
	('3','3 Stars'),
	('4','4 Stars'),
	('5','5 Stars'),
	)
	
	#user = models.ForiegnKey(MyUser,on_delete=models.CASCADE)
	category = models.ForeignKey(Category,on_delete=models.CASCADE)
	name = models.CharField(max_length = 100)
	price = models.FloatField()
	description = models.CharField(max_length = 100)
	stock_status = models.CharField(max_length = 100, choices = STOCK)
	rating = models.CharField(max_length = 100, choices = STARS)
	date_created = models.DateTimeField(auto_now_add = True)
	
	class Meta:
		ordering = ['category','name']
	
	def __str__(self):
		return self.name
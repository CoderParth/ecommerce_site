from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.utils import timezone
from django import forms

# Create your models here.
class Profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.user.username}'

class Address(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	address_line = models.CharField(max_length=100)
	zip_code = models.CharField(max_length=12)
	city = models.CharField(max_length=1024)
	country = models.CharField(max_length=30)

	def __str__(self):
		return f'{self.address_line}'

class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	date_ordered = models.DateTimeField(default=timezone.now)
	quantity_of_product = models.IntegerField(default=1)

	def __str__(self):
		return f'Ordered by {self.user} - {self.product}'

class Wishlist(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.product}'


class SubscribedUsers(models.Model):
    email = models.CharField(unique=True, max_length=50)
    def __str__(self):
	    return f'{self.email}'

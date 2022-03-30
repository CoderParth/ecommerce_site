from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.utils import timezone

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.product} - {self.quantity}'

    def get_total_price(self):
        products_of_user = Cart.objects.filter(user=self)
        total = 0
        for item in products_of_user:
            total += item.product.product_price
        return total

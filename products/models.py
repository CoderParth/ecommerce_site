from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
	product_name = models.CharField(max_length=50)
	product_summary = models.CharField(max_length=100)
	product_image = models.ImageField(default='default.jpg',upload_to='product_images')
	product_is_featured = models.BooleanField(default=False)
	product_description = models.TextField()
	product_price = models.IntegerField()

	#availability of the product
	STATUS = (
		("AV", "Available"),
    	("NV", "Not Available"),
	)
	product_status = models.CharField(max_length=32, choices=STATUS, default='AV')
	product_added_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'{self.product_name}'

	def get_avg_rating(self):
		reviews = Review.objects.filter(product=self)
		count = len(reviews)
		sum = 0
		for rvw in reviews:
			sum += rvw.ratings
		avg_rating = (sum//count)
		range_of_rating = range(0, avg_rating)
		return range_of_rating


class Review(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	review_date = models.DateTimeField(default=timezone.now)
	review_text = models.TextField(max_length=3000 , blank=True)

	#CHOICES FOR RATINGS
	RATING_CHOICES = (
    (1, "Very Poor"),
    (2, "Poor"),
    (3, "Good"),
    (4, "Very Good"),
    (5, "Excellent"),
)
	ratings = models.IntegerField(choices=RATING_CHOICES)

	def __str__(self):
		return f'By {self.user} for {self.product} - {self.ratings}'

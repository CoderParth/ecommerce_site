from django.shortcuts import render, redirect, reverse
from products.models import Product, Review
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from users.models import Wishlist, SubscribedUsers, Order
from django.contrib import messages
from cart.models import Cart
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.
def index(request):
	all_products = Product.objects.all()
	context = {
		'all_products': all_products,

	}
	return render(request, 'products/index.html', context)

def product_detail(request, **kwargs):
	product_id = kwargs['pk']
	product = Product.objects.get(id=product_id)
	context = {
		'product_id': product_id,
		'product': product,
		'all_reviews': product.review_set.all(),
		'total_no_of_reviews': len(product.review_set.all()),
		'average_rating': product.get_avg_rating() #From models, gives a range(start,end)
		}
	return render(request, 'products/product_detail.html', context)

@login_required
def add_review(request):
	if request.method == 'POST':
		product_id =  request.POST['product_id']
		product = Product.objects.get(id=product_id)
		review_text = request.POST['review_text']
		ratings = request.POST['ratings']
		#getting the product
		new_review = Review(user= request.user, product=product, review_text=review_text, ratings=ratings)
		new_review.save()
		print(new_review)
		messages.success(request, 'Your review was submitted')
		return redirect(reverse('product_detail', kwargs={ 'pk': product_id }))


@login_required
def add_to_wishlist(request):
	if request.method == 'POST':
		product_id =  request.POST['product_id']
		product = Product.objects.get(id=product_id)
		wishlist = Wishlist(user=request.user, product=product)
		wishlist.save()
		messages.success(request, 'Item added to wishlist')
		return redirect('index')

#For subscribing to newsletters
def subscribe(request):
	if request.method == 'POST':
		email_address = request.POST['email']
		if SubscribedUsers.objects.filter(email__contains=email_address):
			messages.warning(request, 'You have already been subscribed')
			return redirect('index')
		else:
			subscriber = SubscribedUsers(email=email_address)
			subscriber.save()
			messages.success(request, "Thanks for subscribing")
			return redirect('index')

#for cart items
@login_required
def add_to_cart(request):
	if request.method == 'POST':
		product_id = request.POST['product_id']
		product = Product.objects.get(id=product_id)
		add_to_cart = Cart(user=request.user, product=product, quantity=1)
		add_to_cart.save()
		messages.success(request, "Item added to cart")
		return redirect('index')

#Checkout page
@login_required
def checkout(request):
	checkout_products = request.user.cart_set.all()

	context = {
		'checkout_products' : checkout_products,
		'total_price': Cart.get_total_price(request.user)
	}

	return render(request, 'products/checkout.html', context)


# for removing items in cart
@login_required
def remove_item(request):
	if request.method == 'POST':
		product_id= request.POST['product_id']
		checkout_products = request.user.cart_set.all()
		product_to_remove = checkout_products.filter(product=product_id)
		print(product_to_remove)
		product_to_remove.delete()

		return redirect('checkout')

# for placing an order
@login_required
def place_order(request):
	if request.method == 'POST':
		amount = request.POST['amount']
		if int(amount) > 0:
			context = {
				'amount' : amount,
			}
			return render(request, 'products/stripe_payment.html', context )
		else:
			messages.warning(request, 'Cart cannot be empty')
			return redirect('checkout')

def charge(request):


	if request.method == 'POST':
		print('Data:', request.POST)

		amount = int(request.POST['amount'])

		customer = stripe.Customer.create(
			email=request.user.email,
			name=request.user.username,
			source=request.POST['stripeToken']
			)

		charge = stripe.Charge.create(
			customer=customer,
			amount=amount*100,
			currency='aud',
			description="Online Product"
			)

	return redirect(reverse('success', args=[amount]))


def successMsg(request, args):
	amount = args
	checkout_products = request.user.cart_set.all()
	for item in checkout_products:
		order = Order(user=request.user, product=item.product, quantity_of_product=item.quantity)
		order.save()
	checkout_products.delete()


	context = {
		'amount' : amount,
		'ordered_products': request.user.order_set.all()
	}
	return render(request, 'products/success.html', context)

#for searching products
def search(request):
	searched_product = request.GET.get('search', False)
	all_products = Product.objects.all()
	filtered_product = all_products.filter(product_name__icontains=searched_product)
	print(filtered_product)
	if filtered_product:
		context = {
			'searched_product': searched_product,
			'filtered_list': filtered_product
		}
		return render(request, 'products/search.html', context)

	else:
		return render(request, 'products/404.html', {'searched_product': searched_product})

def sort(request):
	all_products = Product.objects.all()
	searched_product_for_sort = request.GET.get('searched_product_for_sort')
	sort = request.GET.get('sort')
	#for sorting
	if sort:
		filtered_product = all_products.filter(product_name__icontains=searched_product_for_sort)
		if sort == 'lowest to highest':
			sorted_products = filtered_product.order_by('product_price')
		elif sort == 'highest to lowest':
			sorted_products = filtered_product.order_by('-product_price')
		elif sort == 'none':
			context = {
				'searched_product': searched_product_for_sort,
				'filtered_list': filtered_product
			}
			return render(request, 'products/search.html', context)
		# using this context as default if sort exists..
		context = {
				'searched_product': searched_product_for_sort,
				'filtered_list': sorted_products,
				'sort': sort
			}
		return render(request, 'products/search.html', context)

def price_sort(request):
	all_products = Product.objects.all()
	price_min = request.GET.get('price_min')
	price_max = request.GET.get('price_max')
	searched_product = request.GET.get('searched_product')
	filtered_product = all_products.filter(product_name__icontains=searched_product)
	filtered_with_price = filtered_product.filter(product_price__range=(price_min, price_max))
	context = {
		'searched_product': searched_product,
		'filtered_list': filtered_with_price
	}
	return render(request, 'products/search.html', context)

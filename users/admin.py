from django.contrib import admin
from .models import Address, Order, Wishlist, SubscribedUsers
# Register your models here.
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Wishlist)
admin.site.register(SubscribedUsers)

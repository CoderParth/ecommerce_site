"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from products import views as product_views
from django.conf import settings
from django.conf.urls.static import static
from users import views as users_views

#for login view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product_views.index, name='index'),
    path('product_detail/<int:pk>/', product_views.product_detail, name='product_detail'),
    path('add_review/', product_views.add_review, name='add_review'),
    path('add_to_wishlist/', product_views.add_to_wishlist, name='add_to_wishlist'),
    path('register/', users_views.register, name='register'),
    path('profile/', users_views.profile, name='profile'),
    path('profile_edit/', users_views.profile_edit, name='profile_edit'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('subscribe/', product_views.subscribe, name='subscribe'),
    path('add_to_cart/', product_views.add_to_cart, name='add_to_cart'),
    path('checkout/', product_views.checkout, name='checkout'),
    path('remove_item/', product_views.remove_item, name='remove_item'),
    path('place_order/', product_views.place_order, name='place_order'),
    path('charge/', product_views.charge, name='charge'),
    path('success/<str:args>/', product_views.successMsg, name="success"),
    path('search/', product_views.search, name='search'),
    path('sort/', product_views.sort, name='sort'),
    path('price_filter/', product_views.price_sort, name='price_sort'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

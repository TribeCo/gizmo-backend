from importlib.metadata import requires
from typing_extensions import Required
from urllib.request import Request
from rest_framework import serializers
from .models import *
from accounts.models import User
from products.models import Product
#---------------------------
class ProductSerializerForCart(serializers.ModelSerializer):
    discount_price = serializers.CharField(source='discounted_price')
    class Meta:
        model = Product
        fields = ('id','name', 'image1', 'code', 'price', 'price', 'discount', 'discounted','discount_price')
#---------------------------
class ColorSerializerForCart(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id','name', 'en', 'code')
#---------------------------
class UserSerializerForCart(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phoneNumber', 'full_name','id')
#---------------------------
class CartItemSerializerForCart(serializers.ModelSerializer):
    product = ProductSerializerForCart()
    color = ColorSerializerForCart()
    class Meta:
        model = CartItem
        fields = ['id','quantity','color','product'] 
#--------------------------- 
class CartSerializer(serializers.ModelSerializer):
    user = UserSerializerForCart(required=False)
    items = CartItemSerializerForCart(many=True)
    class Meta:
        model = Cart
        fields = ['get_total_price','id','user','items',]
#---------------------------
class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ['id','quantity','color','product']  
#---------------------------
class CartItemUpdateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),required=False)

    class Meta:
        model = CartItem
        fields = ['quantity','color','product']  
#---------------------------
class CouponSerializer(serializers.ModelSerializer):
    valid = serializers.CharField(source='is_valid', required=False)
    
    class Meta:
        model = Coupon
        fields = ['code','valid_from','valid_to','discount','valid']  
#---------------------------
from importlib.metadata import requires
from rest_framework import serializers
from .models import *
from accounts.models import User
from products.models import Product
#---------------------------
class ProductSerializerForCart(serializers.ModelSerializer):
    discount_price = serializers.CharField(source='discounted_price')
    class Meta:
        model = Product
        fields = ('name', 'image', 'code', 'price', 'id', 'price', 'discount', 'discounted','discount_price')
#---------------------------
class ColorSerializerForCart(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('name', 'en', 'code')
#---------------------------
class UserSerializerForCart(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phoneNumber', 'full_name')
#---------------------------
class CartItemSerializerForCart(serializers.ModelSerializer):
    product = ProductSerializerForCart()
    color = ColorSerializerForCart()
    class Meta:
        model = CartItem
        fields = ['quantity','color','product'] 
#--------------------------- 
class CartSerializer(serializers.ModelSerializer):
    user = UserSerializerForCart(required=False)
    items = CartItemSerializerForCart(many=True)
    class Meta:
        model = Cart
        fields = ['user','items']
#---------------------------
class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)
    
    class Meta:
        model = CartItem
        fields = ['quantity','color','product']  
#---------------------------
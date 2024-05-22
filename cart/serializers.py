from importlib.metadata import requires
from typing_extensions import Required
from urllib.request import Request
from rest_framework import serializers
from .models import *
from accounts.models import User
from products.models import Product
from config.settings import DOMAIN
#---------------------------
class ProductSerializerForCart(serializers.ModelSerializer):
    discount_price = serializers.IntegerField(source='discounted_price_int')
    image1 = serializers.SerializerMethodField()

    def get_image1(self, obj):
        image_url = '{}{}'.format(DOMAIN, obj.image1.url) if obj.image1 else None
        return image_url

    class Meta:
        model = Product
        fields = ('id','name', 'image1', 'code', 'price', 'price', 'discount', 'discounted','discount_price')
#---------------------------
class ColorSerializerForCart(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id','name', 'en', 'code')
#---------------------------
class CouponSerializer(serializers.ModelSerializer):
    valid = serializers.CharField(source='is_valid', required=False)
    
    class Meta:
        model = Coupon
        fields = ['code','valid_from','valid_to','discount','valid']  
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
class CartItemSerializerLocalForCart(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id','color','product','quantity'] 
#--------------------------- 
class CartLocalSerializer(serializers.ModelSerializer):
    items = CartItemSerializerLocalForCart(many=True)
    class Meta:
        model = Cart
        fields = ['id','items',]
#---------------------------
class CartSerializer(serializers.ModelSerializer):
    user = UserSerializerForCart(required=False)
    items = CartItemSerializerForCart(many=True)
    total_price_method = serializers.IntegerField(source='total_price')
    delta_discounted_method = serializers.IntegerField(source='delta_discounted')
    total_discounted_price_method = serializers.IntegerField(source='total_discounted_price')
    coupon_discount = serializers.IntegerField(source='get_discount_coupon')
    coupon = CouponSerializer()
    class Meta:
        model = Cart
        fields = ['total_price_method','coupon_discount','total_discounted_price_method','delta_discounted_method','id','user','items','coupon']
#---------------------------
class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ['id','quantity','color','product','is_sync']  
#---------------------------
class CartItemUpdateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),required=False)

    class Meta:
        model = CartItem
        fields = ['quantity','color','product']  
#---------------------------
class TempCartItemOneSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = TempCartItem
        fields = ['id','quantity','color','product']  
#---------------------------
class TempCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializerForCart()
    color = ColorSerializerForCart()
    class Meta:
        model = TempCartItem
        fields = ['id','quantity','color','product']  
#---------------------------
class TempCartSerializer(serializers.ModelSerializer):
    total_price_method = serializers.IntegerField(source='total_price')
    delta_discounted_method = serializers.IntegerField(source='delta_discounted')
    total_discounted_price_method = serializers.IntegerField(source='total_discounted_price')
    temp_items = TempCartItemSerializer(many=True)
    class Meta:
        model = TempCart
        fields = ['total_price_method','total_discounted_price_method','delta_discounted_method','id','temp_items',]
#---------------------------
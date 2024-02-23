from rest_framework import serializers
from .models import *
from accounts.models import User
#---------------------------
class ProductSerializerForCart(serializers.ModelSerializer):
    discount_price = serializers.CharField(source='discounted_price')
    class Meta:
        model = Product
        fields = ('name', 'image', 'price', 'id', 'price', 'discount', 'discounted','discount_price')
#---------------------------
class OrderItemsSerializerForOrder(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'price', 'quantity',)
#---------------------------
class UserSerializerForOrder(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phoneNumber', 'full_name')
#---------------------------
class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializerForOrder(required=False)
    items = OrderItemsSerializerForOrder(many=True)
    class Meta:
        model = Order
        fields = ('created','updated','paid', 'discount', 'receipt', 'receipt_bool', 'ref_id', 'authority', 'address', 'processed', 'packing', 'shipped', 'deliveried' )
#---------------------------
class OrderItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializerForCart()
    class Meta:
        model = OrderItem
        fields = ('product', 'price', 'quantity',)
#---------------------------

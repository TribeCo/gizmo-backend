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
class AddressSerializerForOrder(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['province','city','straight_address', 'postal_code','current']
#---------------------------
class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializerForOrder(required=False)
    items = OrderItemsSerializerForOrder(many=True)
    address = AddressSerializerForOrder()
    class Meta:
        model = Order
        fields = ('user' ,'address','items','shamsi_date','paid', 'discount', 'ref_id'
        , 'authority', 'address', 'processed', 'packing', 'shipped', 
        'deliveried', 'total_price', 'discount_string',
        'discount_amount' ,'pay_amount')
#---------------------------
class OrderDashBoardSerializer(serializers.ModelSerializer):
    user = UserSerializerForOrder(required=False)
    address = AddressSerializerForOrder()
    class Meta:
        model = Order
        fields = ('user' ,'address','shamsi_date', 'discount', 'ref_id', 'address', 'processed', 'packing', 'shipped', 
        'deliveried', 'total_price', 'discount_string',
        'discount_amount' ,'pay_amount','recipient')
#---------------------------
class OrderItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializerForCart()
    class Meta:
        model = OrderItem
        fields = ('product', 'price', 'quantity',)
#---------------------------

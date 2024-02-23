from rest_framework import serializers
from .models import *

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
                    'created',
                    'updated',
                    'paid', 
                    'discount', 
                    'receipt', 
                    'receipt_bool', 
                    'ref_id', 
                    'authority', 
                    'address', 
                    'processed', 
                    'packing', 
                    'shipped', 
                    'deliveried'
                )
#---------------------------
class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

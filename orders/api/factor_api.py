from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from ..serializers import FactorSerializer, OrderSerializer, OrderItemsSerializer
from ..models import Order, OrderItem
#---------------------------
"""
    The codes related to the site's orders are in this app.
    api's in factor_api.py :

    1- GenerateFactor --> this api generate a factor for order with id.

"""
#---------------------------
message_for_front = {
    'order_created': 'سفارش ثبت شد',
    'order_not_found': 'سفارش یافت نشد.',
    'order_item_not_found': 'آیتم سفارش یافت نشد',
    'order_updated': 'سفارش با موفقیت آپدیت شد.',
    'no_cart_items_in_user_cart': 'سبد کاربر خالی می باشد',
    'cart_converted_to_order': 'سفارشات ثبت شدند',
}
#---------------------------
class GenerateFactor(APIView):

    def post(self,request):

        pk = request.data.get('id')       

        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({'message':message_for_front['order_not_found']}, status=status.HTTP_400_BAD_REQUEST)

        if(order.factor == None):
            order.create_factor()
            
        info = FactorSerializer(order)

        return Response({'data':info.data}, status=status.HTTP_200_OK)
#---------------------------

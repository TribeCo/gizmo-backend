from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import OrderSerializer, OrderItemsSerializer
from .models import Order

message_for_front = {
    'order_created': 'سفارش ثبت شد',
    'order_item_not_found': 'آیتم سفارش یافت نشد',
}

class CreateOrderAPIView(APIView):
    def post(self, request):
        user = request.user
        serializer = OrderSerializer(data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response({'message': message_for_front['order_created']}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ReadOrderAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
#---------------------------
class ListOrdersAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
#---------------------------
class DeleteOrderAPIView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
#---------------------------
class SetOrderItemsQuantityAPIView(APIView):
    def post(self, request):
        user = request.user
        order_id = request.get('order_id')
        item_id = request.data.get('item_id')
        
        try:
            order = user.orders.get(pk = order_id)
        except:
            return Response(status.HTTP_404_NOT_FOUND)
        
        try:
            item = order.items.get(pk = item_id)
        except:
            return Response(status.HTTP_404_NOT_FOUND)
        
        order.items.remove(item)
        order.save()

        return Response(status=status.HTTP_200_OK)

#---------------------------
class ListOrderItemsAPIview(generics.ListAPIView):
    def get(self,request):
        user = request.user
        order_id = request.data.get('order_id')
        
        try:
            order = user.orders.get(pk = order_id)
        except:
            return Response(status.HTTP_404_NOT_FOUND)
        
        serializer = OrderItemsSerializer(order.items, many=True)

        return Response({'data': serializer.data})
#---------------------------
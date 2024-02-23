from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import OrderSerializer, OrderItemsSerializer
from .models import Order,OrderItem
#---------------------------
"""
    The codes related to the site's orders are in this app.
    api's in api_views.py :

    1- CreateOrderAPIView --> 
    2- ReadOrderAPIView --> 
    3- ListOrdersAPIView -->
    4- DeleteOrderAPIView --> 

"""
#---------------------------
message_for_front = {
    'order_created': 'سفارش ثبت شد',
    'order_not_found': 'سفارش یافت نشد.',
    'order_item_not_found': 'آیتم سفارش یافت نشد',
    'order_updated': 'سفارش با موفقیت آپدیت شد.',
}
#---------------------------
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
        order_id = request.data.get('order_id')
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity')
        
        try:
            order = user.orders.get(id = order_id)
        except:
            return Response({'message':message_for_front['order_not_found']},status.HTTP_404_NOT_FOUND)
        
        try:
            item = order.items.get(id = item_id)
        except:
            return Response({'message':message_for_front['order_item_not_found']},status.HTTP_404_NOT_FOUND)
        
        item.quantity = quantity
        item.save()

        return Response({'message':message_for_front['order_updated']},status=status.HTTP_200_OK)
#---------------------------
class ListOrderItemsAPIview(APIView):
    def post(self,request,pk):
        try:
            order = Order.objects.get(id = pk)
        except Order.DoesNotExist:
            return Response({'message':message_for_front['order_not_found']},status.HTTP_404_NOT_FOUND)
        
        serializer = OrderItemsSerializer(order.items, many=True)

        return Response({'data': serializer.data})
#---------------------------
class DeleteProductToOrderAPIView(APIView):
    """Remove a product from the order"""
    def delete(self, request,pk):
        try:
            item = OrderItem.objects.get(id=pk)
        except OrderItem.DoesNotExist:
            return Response({'message':message_for_front['order_item_not_found']}, status=status.HTTP_404_NOT_FOUND)    

        item.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT) 
#---------------------------
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from ..serializers import OrderSerializer, OrderItemsSerializer
from ..models import Order, OrderItem
#---------------------------
"""
    The codes related to the site's orders are in this app.
    api's in api_views.py :

    1- CreateOrderAPIView --> Creats an order with post method
    2- ReadOrderAPIView -->  Gets a single order 
    3- ListOrdersAPIView --> Lists all of the orders
    4- DeleteOrderAPIView --> Delets an order with id 
    5- SetOrderItemsQuantityAPIView --> Sets the amount of one single product
    6- ListOrderItemsAPIview --> Lists all items of one order
    7- DeleteProductToOrderAPIView --> Removes a product from the order
    8- ConvertCartToOrderAPIView --> converts an instance of a Cart model to an instance of an Order model

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
class CreateOrderAPIView(APIView):
    """
        creats an order object.
        login is required.        
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        serializer = OrderSerializer(data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response({'message': message_for_front['order_created']}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ReadOrderAPIView(generics.RetrieveAPIView):
    """reads a single order object with ID(domain/.../ID/)"""
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
#---------------------------
class ListOrdersAPIView(generics.ListAPIView):
    """read all of the order objects"""
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
#---------------------------
class DeleteOrderAPIView(generics.DestroyAPIView):
    """deletes a single order object with ID(domain/.../ID/)"""
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
#---------------------------
class SetOrderItemsQuantityAPIView(APIView):
    """
    set the quantity of a item in order.
    login is required.
    required fields{
        order_id
        item_id
        quantity
    }
    """
    permission_classes = [IsAuthenticated]
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
    """Lists all items of an order with order_ID(domaim/.../ID/)"""
    permission_classes = [IsAuthenticated]
    def post(self,request,pk):
        try:
            order = Order.objects.get(id = pk)
        except Order.DoesNotExist:
            return Response({'message':message_for_front['order_not_found']},status.HTTP_404_NOT_FOUND)
        
        serializer = OrderItemsSerializer(order.items, many=True)

        return Response({'data': serializer.data})
#---------------------------
class DeleteProductToOrderAPIView(APIView):
    """Remove a product from the order with ID(domain/.../ID/)"""
    permission_classes = [IsAuthenticated]
    def delete(self, request,pk):
        try:
            item = OrderItem.objects.get(id=pk)
        except OrderItem.DoesNotExist:
            return Response({'message':message_for_front['order_item_not_found']}, status=status.HTTP_404_NOT_FOUND)    

        item.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT) 
#---------------------------
class ConvertCartToOrderAPIView(APIView):
    """
        converts a cart to order.
        login required.        
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        cart = user.cart
        try:
            cart_items = cart.items.all()
        except:
            return Response({'message': message_for_front['no_cart_items_in_user_cart']}, status=status.HTTP_404_NOT_FOUND)
        
        order = Order(user = user)        

        for item in cart_items:
            order_item = OrderItem()
            order_item.product = item.product
            order_item.price = item.price
            order_item.quantity = item.quantity
            order_item.save()
            order.orders.add(order_item)
        order.save()
        
        for item in cart_items:
            item.delete()
        
        return Response({'message': message_for_front['cart_converted_to_order']})
#---------------------------
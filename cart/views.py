from email import message
from itertools import product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem,Cart
from .serializers import *
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
#---------------------------
"""
    The codes related to the site's cart are in this app.
    api's in api_views.py :

    1- CartDetailAPIView --> Getting the user's shopping cart information
    2- AddProductToCartAPIView --> Add a product to the cart
    3- DeleteProductToCartAPIView --> Remove a product from the cart
    4- UpdateBannerAPIView --> update banner with id

"""
#---------------------------
messages_for_front = {
    'banner_created' : 'بنر جدید ایجاد شد',
    'item_not_found' : 'محصول یافت نشد.',
    'add_product' : 'محصول با موفقیت به سبد خرید اضافه شد.',
    'update_product' : 'محصول آپدیت شد.',
    
}
#---------------------------
class CartDetailAPIView(APIView):
    """Getting the user's shopping cart information"""
    def get(self, request):
        serializer = CartSerializer(request.user.cart)
        return Response({'cart':serializer.data}, status=status.HTTP_200_OK)
#---------------------------
class AddProductToCartAPIView(APIView):
    """Add a product to the cart"""
    def post(self, request,):
        
        serializer = CartItemSerializer(data=request.data)

        cart = request.user.cart

        if serializer.is_valid():
            
            item = serializer.save(cart=cart,price=0)
            item.price = item.product.discounted_price_int
            item.save()
            return Response({'message':messages_for_front['add_product']}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
#---------------------------
class DeleteProductToCartAPIView(APIView):
    """Remove a product from the cart"""
    def delete(self, request,pk):
        try:
            item = CartItem.objects.get(id=pk)
        except CartItem.DoesNotExist:
            return Response({'message':messages_for_front['item_not_found']}, status=status.HTTP_404_NOT_FOUND)    

        item.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT) 
#---------------------------
class CartItemUpdateView(APIView):
    """Update Cart item information with ID"""
    def put(self, request,pk):
        try:
            item = CartItem.objects.get(id=pk)
        except CartItem.DoesNotExist:
            return Response({'message':messages_for_front['item_not_found']}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartItemSerializer(data=request.data,instance=item)
        
        if serializer.is_valid():
            return Response({'message':messages_for_front['update_product'],'item':serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
#---------------------------
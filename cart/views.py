from itertools import product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem,Cart
from .serializers import *
#---------------------------
"""
    The codes related to the site's cart are in this app.
    api's in api_views.py :

    1- CartDetailAPIView --> Getting the user's shopping cart information
    2- AddProductToCartAPIView --> Add a product to the cart
    3- DeleteBannerAPIView --> delete banner with id
    4- UpdateBannerAPIView --> update banner with id

"""
#---------------------------
messages_for_front = {
    'banner_created' : 'بنر جدید ایجاد شد',
    'product_not_found' : 'محصول یافت نشد.',
    'add_product' : 'محصول با موفقیت به سبد خرید اضافه شد.',
    
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
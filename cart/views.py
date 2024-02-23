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
    2- ReadBannerBySlugAPIView --> read banner api with for what input
    3- DeleteBannerAPIView --> delete banner with id
    4- UpdateBannerAPIView --> update banner with id

"""
#---------------------------
messages_for_front = {
    'banner_created' : 'بنر جدید ایجاد شد',
    'banner_not_found' : 'بنر یافت نشد',
    'banner_deleted' : 'بنر حذف شد',
    
}
#---------------------------
class CartDetailAPIView(APIView):
    """Getting the user's shopping cart information"""
    def get(self, request):
        serializer = CartSerializer(request.user.cart)
        return Response({'cart':serializer.data}, status=status.HTTP_200_OK)
#---------------------------
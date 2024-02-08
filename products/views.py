
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import Brand
from django.utils import timezone
from datetime import date
#---------------------------
"""
    The codes related to the site's products are in this app.
    api's in api_views.py :

    1- BrandCreateAPIView --> create a brand
    2- FoodAllListAPIView --> List of all foods
    3- FoodDetailView  --> Getting the information of a food with ID
    4- FoodDeleteView --> Remove a food with an ID
    5- FoodUpdateView --> Update food information with ID

"""
#---------------------------
messages_for_front = {
    'brand_created' : 'برند جدید ساخته شد.',
    'food_reserved' : 'غذا رزرو شد.',
    'food_is_over' : 'موجودی غذا تمام شده است.',
    'food_not_found' : 'غذا پیدا نشد.',
    'image_updated' : 'عکس اپدیت شد.',
    'food_reservation_updated' : 'رزرو غذا اپدیت شد.',
}
#---------------------------
class BrandCreateAPIView(APIView):
    """
        create a food
        {
            "name": "Asus",
            "slug": "Asus",
            "logo": ,
            "description": "text about brand."
        }
    """
    def post(self, request):
        serializer = BrandSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': messages_for_front['brand_created'],'data' : serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class BrandAllListAPIView(ListAPIView):
    """List of all Brands"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
#---------------------------
class FoodDetailView(RetrieveAPIView):
    """Getting the information of a Brand with ID(domain.com/..../pk/)"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'pk'
#---------------------------
class FoodDeleteView(DestroyAPIView):
    """Remove a Brand with an ID(domain.com/..../pk/)"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'pk'
#---------------------------
class FoodUpdateView(UpdateAPIView):
    """Update Brand information with ID(domain.com/..../pk/)"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'pk'
#---------------------------
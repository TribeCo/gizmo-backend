from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from products.serializers import *
from products.models import Brand
#---------------------------
"""
    The codes related to the site's products are in this app.
    api's in api_views.py :

    1- BrandCreateAPIView --> create a brand
    2- BrandAllListAPIView --> List of all brand
    3- BrandDetailView  --> Getting the information of a brand with ID
    4- BrandDeleteView --> Remove a brand with an ID
    5- BrandUpdateView --> Update brand information with ID

"""
#---------------------------
messages_for_front = {
    'brand_created' : 'برند جدید ساخته شد.',
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
    permission_classes = [IsAuthenticated]
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
class BrandDetailView(RetrieveAPIView):
    """Getting the information of a Brand with ID(domain.com/..../pk/)"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'pk'
#---------------------------
class BrandDeleteView(DestroyAPIView):
    """Remove a Brand with an ID(domain.com/..../pk/)"""
    permission_classes = [IsAuthenticated]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'pk'
#---------------------------
class BrandUpdateView(UpdateAPIView):
    """Update Brand information with ID(domain.com/..../pk/)"""
    permission_classes = [IsAuthenticated]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'pk'
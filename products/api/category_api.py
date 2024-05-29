from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from products.serializers import *
#---------------------------
"""
    The codes related to the site's products are in this app.
    api's in api_views.py :

    1- CategoryCreateAPIView --> Create a Category
    2- CategoryDetailAPIView --> Getting the information of a Category with ID
    3- CategoryListAPIView --> List of all Category
    4- CategoryDeleteAPIView --> Remove a Category with an ID
    5- CategoryUpdateAPIView --> Update Category information with ID
    6- CategoryProductsListAPIView --> Retrieve a list of products belonging to a specific category
    7- CategotyLandingListAPIView --> Retrieve a list of categories for landing page

"""
#---------------------------
messages_for_front = {
    'category_created': 'دسته جدید ساخته شد',
    'category_not_found': 'دسته مورد نظر وجود ندارد',
    'categoty_for_landing_not_found': 'دسته ای فعال برای صفحه لندینگ وجود ندارد',
    }
#---------------------------
class CategoryCreateAPIView(APIView):
    """
    Create a Category
    
        {
            "name":
            "slug":   
        }
    
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):    
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': messages_for_front['category_created']})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class CategoryDetailAPIView(RetrieveAPIView):
    """Getting the information of a Category with ID(domain.com/..../pk/)"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
#---------------------------
class CategoryListAPIView(ListAPIView):
    """List of all Category"""
    serializer_class  = CategorySearchSerializer
    queryset = Category.objects.all()
#---------------------------
class CategoryDeleteAPIView(DestroyAPIView):
    """Remove a Category with an ID(domain.com/..../pk/)"""
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
#---------------------------
class CategoryUpdateAPIView(UpdateAPIView):
    """Update Category information with ID(domain.com/..../pk/)"""
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
#---------------------------
class CategoryProductsListAPIView(APIView):
    """Retrieve a list of products belonging to a specific category"""
    def get(self, request, category_name):
        try:
            category = Category.objects.get(slug = category_name)
        except:
            return Response({'message':messages_for_front['category_not_found']}, status=status.HTTP_404_NOT_FOUND)

        articles = category.products.all()
        serializer = ProductSliderSerializer(articles, many=True)

        return Response({'data': serializer.data})
#---------------------------
class CategotyLandingListAPIView(APIView):
    """Retrieve a list of categories for landing page"""
    def get(self, request):        
        try:
            catgories = Category.objects.filter(is_for_landing=True)[:4]
        except:
            return Response({'message': messages_for_front['categoty_for_landing_not_found']}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategoryLandingSerializer(catgories, many=True)

        return Response({'data': serializer.data})
#---------------------------
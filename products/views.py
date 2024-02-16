from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import Brand
from django.utils import timezone
from datetime import timedelta
from accounts.models import WatchedProduct
#---------------------------
"""
    The codes related to the site's products are in this app.
    api's in api_views.py :

    1- BrandCreateAPIView --> create a brand
    2- BrandAllListAPIView --> List of all brand
    3- BrandDetailView  --> Getting the information of a brand with ID
    4- BrandDeleteView --> Remove a brand with an ID
    5- BrandUpdateView --> Update brand information with ID

    6- NewProductAPIView --> get 10 New Product
    7- ObservedProductAPIView --> This API returns the user's viewed products

"""
#---------------------------
messages_for_front = {
    'brand_created' : 'برند جدید ساخته شد.',
    'product_created': 'محصول جدید ساخته شد',
    'category_created': 'دسته جدید ساخته شد',
    'category_not_found': 'دسته مورد نظر وجود ندارد',
    'product_not_found' : 'محصول مورد نظر وجود ندارد.',
    'categoty_for_landing_not_found': 'دسته ای فعال برای صفحه لندینگ وجود ندارد',
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
class BrandDetailView(RetrieveAPIView):
    """Getting the information of a Brand with ID(domain.com/..../pk/)"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'pk'
#---------------------------
class BrandDeleteView(DestroyAPIView):
    """Remove a Brand with an ID(domain.com/..../pk/)"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'pk'
#---------------------------
class BrandUpdateView(UpdateAPIView):
    """Update Brand information with ID(domain.com/..../pk/)"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'pk'
#---------------------------
    """Products API views"""

class ProductCreateAPIView(APIView):
    """Create a Product"""
    def post(self, request):    
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': messages_for_front['product_created']})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ProductDetailAPIView(APIView):
    """Getting the information of a Product with ID(domain.com/..../pk/)"""
    def get(self, request,pk):    
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({'message': messages_for_front['product_not_found']}, status=status.HTTP_404_NOT_FOUND)
        
        if(request.user.is_authenticated):
            wp = WatchedProduct(user=request.user,product=product)
            wp.save()

        serializer = ProductSerializer(product)

        return Response(serializer.data)
    
#---------------------------
class ProductDetailAPIViewBySlug(APIView):
    """Getting the information of a Product with slug(domain.com/..../slug/)"""
    def get(self, request,slug):    
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Response({'message': messages_for_front['product_not_found']}, status=status.HTTP_404_NOT_FOUND)

        if(request.user.is_authenticated):
            wp = WatchedProduct(user=request.user,product=product)
            wp.save()

        serializer = ProductSerializer(product)
        
        return Response(serializer.data)
#---------------------------
class ProductListAPIView(ListAPIView):
    """List of all Products"""    
    serializer_class  = ProductSerializer
    queryset = Product.objects.all()
#---------------------------
class ProductDeleteAPIView(DestroyAPIView):
    """Remove a Product with an ID(domain.com/..../pk/)"""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
#---------------------------
class ProductUpdateAPIView(UpdateAPIView):
    """Update Product information with ID(domain.com/..../pk/)"""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
#---------------------------
class NewProductAPIView(APIView):
    """get 10 New Product"""
    def get(self, request):    
        four_days_ago = timezone.now() - timedelta(days=4)
        new_products = Product.objects.filter(updated__gte=four_days_ago)
        serializer = ProductSerializer(new_products,many=True)
        return Response(serializer.data)
#---------------------------
class ObservedProductAPIView(APIView):
    """This API returns the user's viewed products"""
    permission_classes = [IsAuthenticated]
    def get(self, request):    
        watched = WatchedProduct.objects.filter(user = request.user)
        products = []
        for wp in watched:
            products.append(wp.product)

        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)
#---------------------------  
#Category API views
    
class CategoryCreateAPIView(APIView):
    """Create a Category"""
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
    serializer_class  = CategorySerializer
    queryset = Category.objects.all()
#---------------------------
class CategoryDeleteAPIView(DestroyAPIView):
    """Remove a Category with an ID(domain.com/..../pk/)"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
#---------------------------
class CategoryUpdateAPIView(UpdateAPIView):
    """Update Category information with ID(domain.com/..../pk/)"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
#---------------------------
class CategoryProductsListAPIView(APIView):
    def get(self, request, category_name):
        try:
            category = Category.objects.get(name = category_name)
        except:
            return Response({'message':messages_for_front['category_not_found']}, status=status.HTTP_404_NOT_FOUND)

        articles = category.products.all()
        serializer = CategorySerializer(articles, many=True)

        return Response({'data': serializer.data})
#---------------------------
class CategotyLandingListAPIView(APIView):
    def get(self, request):        
        try:
            catgories = Category.objects.filter(is_for_landing=True)[:4]
        except:
            return Response({'message': messages_for_front['categoty_for_landing_not_found']}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(catgories, many=True)

        return Response({'data': serializer.data})
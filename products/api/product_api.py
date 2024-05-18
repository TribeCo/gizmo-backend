from math import prod
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from products.filters import shop_products
from products.serializers import *
from django.utils import timezone
from datetime import timedelta
from accounts.models import WatchedProduct
#---------------------------
"""
    The codes related to the site's products are in this app.
    api's in api_views.py :

    1- ProductCreateAPIView --> Create a Product
    2- ProductDetailAPIView --> Getting the information of a Product with ID
    3- ProductDetailAPIViewBySlug --> Getting the information of a Product with slug
    4- ProductListAPIView --> List of all Products
    5- ProductDeleteAPIView --> Remove a Product with an ID
    6- ProductUpdateAPIView --> Update Product information with ID
    7- ProductDiscountedListAPIView --> Retrieve a list of discounted products
    8- SimilarProductsAPIView --> Retrieve similar products based on a given product ID
    9- NewProductAPIView --> get 10 New Product
    10- ObservedProductAPIView --> This API returns the user's viewed products
    11- ProductSearchAPIView --> Search for products

"""
#---------------------------
messages_for_front = {
    'product_created': 'محصول جدید ساخته شد',
    'discounted_product_not_found': 'کالای تخفیف خورده وجود ندارد',
    'product_not_found' : 'محصول مورد نظر وجود ندارد.',
    
    }
#---------------------------
class ProductCreateAPIView(APIView):
    """
    Create a Product
    
        {
            "name": 
            "slug": 
            "price": 
            "image": 
            "alt":
            "short_description":
            "description": 
            "more_info": 
        }
    """
    permission_classes = [IsAuthenticated]
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
            # this comment

        serializer = ProductPageSerializer(product)

        data = serializer.data

        return Response(data)    
#---------------------------
class FavProductDetailAPIViewBySlug(APIView):
    """Getting the information of a fav Product with slug(domain.com/..../slug/)"""
    def get(self, request,slug):    
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Response({'message': messages_for_front['product_not_found']}, status=status.HTTP_404_NOT_FOUND)

        if(request.user.is_authenticated):
            if(product in request.user.wishlist.all()):
                is_fav = True
            else:
                is_fav = False

        data = {}

        data['is_fav'] = is_fav
        return Response(data)
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

        serializer = ProductPageSerializer(product)
        data = serializer.data

        return Response(data)
#---------------------------
class ProductListAPIView(ListAPIView):
    """List of all Products"""    
    serializer_class  = ProductSearchSerializer
    queryset = shop_products()
#---------------------------
class ProductDeleteAPIView(DestroyAPIView):
    """Remove a Product with an ID(domain.com/..../pk/)"""
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
#---------------------------
class ProductUpdateAPIView(UpdateAPIView):
    """Update Product information with ID(domain.com/..../pk/)"""
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
#---------------------------
class ProductDiscountedListAPIView(APIView):
    """Retrieve a list of discounted products"""
    def get(self, request):        
        try:
            products = Product.objects.non_dubai().filter(discounted=True)
        except Product.DoesNotExist:
            return Response({"message": messages_for_front['discounted_product_not_found']}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSliderSerializer(products, many=True)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
#---------------------------
class SimilarProductsAPIView(APIView):
    """Retrieve similar products based on a given product ID"""
    def get(self, request,pk):
        ID = pk      
        try:
            product = Product.objects.get(id = ID)
        except Product.DoesNotExist:
            return Response({'message': messages_for_front['product_not_found']}, status=status.HTTP_404_NOT_FOUND)


        similar_products = product.get_similar_products()

        products = ProductSliderSerializer(similar_products, many=True)

        return Response({'data': products.data})
#---------------------------
class NewProductAPIView(APIView):
    """get 10 New Product"""
    def get(self, request):
        new_products = shop_products().order_by('-id')[:4]
        serializer = ProductSliderSerializer(new_products,many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
#---------------------------
class ObservedProductAPIView(APIView):
    """This API returns the user's viewed products"""
    permission_classes = [IsAuthenticated]
    def get(self, request):    
        watched = WatchedProduct.objects.filter(user = request.user)
        products = []
        for wp in watched:
            products.append(wp.product)

        serializer = ProductSliderSerializer(products,many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
#---------------------------
class ProductSearchAPIView(APIView):
    """ Search for products """
    def get(self, request, slug):
        # product = Product.objects.filter(slug=slug)
        products = Product.objects.filter(name__icontains=slug)
        serializer = ProductSerializer(products, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
#---------------------------
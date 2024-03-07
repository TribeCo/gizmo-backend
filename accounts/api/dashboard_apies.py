from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import Product
from inquiry.models import ForeignOrder
from orders.models import Order
from products.serializers import *
from rest_framework.permissions import IsAuthenticated
#---------------------------
"""
    The codes related to the site's products are in this app.
    api's in api_views.py :

    1- UserCreateAPIView --> create a user
    2- UserRetrieveAPIView --> read one user with id
    3- UserListAPIView --> read all user
    4- UserDeleteAPIView --> delete one user with id
    5- UserUpdateAPIView --> update one user with id
    6- CreateCommentForArticleAPIView --> create comment for article
    7- CreateCommentForProductAPIView --> create comment for product
    8- ReadCommentForProductAPIView --> read comment for a product
    9- ReadCommentForarticleAPIView --> read comment for a article
    10- DeleteCommentAPIView --> delete comment with id
    11- UpdateCommentAPIView --> update comment with id
    12- CreateAddressAPIView --> create an address
    13- ReadAddressAPIView --> read all addresses
    14- UpdateAddressAPIView --> update address with id
    15- DeleteAddressAPIView --> delete address with id

"""
#---------------------------
messages_for_front = {
    'user_created' : 'کاربر جدید ایجاد شد.',
    'user_not_found' : 'کاربر یافت نشد',
    'article_not_found' : 'مقاله یافت نشد',
    'product_not_found' : 'محصول یافت نشد',
    'comment_not_found' : 'نظر یافت نشد',
    'comment_deleted' : 'نظر حذف شد',
    'user_found' : 'کاربر یافت شد.',
    'password_changed' : 'پسورد با موفقیت تغییر کرد.',
    'wrong_coode' : 'کد اعتبارسنجی نامعتبر است.',
    'right_code' : 'کد اعتبارسنجی صحیح است.',
    'code_sent' : 'کد ارسال شد.',
    'favorite_products_not_found': 'محصول مورد علاقه ای وجود ندارد',
    'product_added_to_wishlist': 'محصول به لیست مورد علاقه‌ها اضافه شد',
    'product_removed_from_wishlist': 'محصول از لیست مورد علاقه‌ها حذف شد',
    'not_id' : 'آیدی مورد نیاز است.',
    'product_removed_from_informing' : 'محصول از لیست انتظار حذف شد.',
    'product_added_to_informing' : 'محصول به لیست انتظار اضافه شد.',
    
}
#---------------------------
class FavoriteProductsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):        
        user = request.user        
        try:
            products = user.wishlist.all()
        except:
            return Response({'message': messages_for_front['favorite_products_not_found']}, status=status.HTTP_404_NOT_FOUND)
        

        favorite_products = ProductSliderSerializer(products, many=True)
        return Response({'data': favorite_products.data})
#---------------------------
class AddFavoriteProductAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        pk = request.data.get('id')

        if(not pk):
            return Response({'message': messages_for_front['not_id']}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        try:
            product = Product.objects.get(pk = pk)
        except:
            return Response({'message': messages_for_front['product_not_found']}, status=status.HTTP_404_NOT_FOUND)
        
        user.wishlist.add(product)
        user.save()

        return Response({'message': messages_for_front['product_added_to_wishlist']},status=status.HTTP_200_OK)
#---------------------------
class DeleteFvaoriteProductAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        pk = request.data.get('id')

        if(not pk):
            return Response({'message': messages_for_front['not_id']}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        try:
            product = Product.objects.get(pk = pk)
        except:
            return Response({'message': messages_for_front['favorite_products_not_found']}, status=status.HTTP_404_NOT_FOUND)
    
        user.wishlist.remove(product)
        user.save()

        return Response({'message': messages_for_front['product_removed_from_wishlist']}, status=status.HTTP_200_OK)
#---------------------------
class UserOrdersCountAPIView(APIView):
    """Retrieve the count of orders and returns for the logged-in user"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_authenticated:
            orders_count = Order.objects.filter(user=request.user).count()
            returns_count = Order.objects.filter(user=request.user, returned=True).count()
            foreign_returns_count = ForeignOrder.objects.filter(user=request.user).count()
            return Response({'orders_count': orders_count, 'returns_count': returns_count, 'foreign_returns_count': foreign_returns_count}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
#---------------------------
class AddInformingProductAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        pk = request.data.get('id')

        if(not pk):
            return Response({'message': messages_for_front['not_id']}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        try:
            product = Product.objects.get(pk = pk)
        except:
            return Response({'message': messages_for_front['product_not_found']}, status=status.HTTP_404_NOT_FOUND)
        
        user.informing.add(product)
        user.save()

        return Response({'message': messages_for_front['product_added_to_informing']},status=status.HTTP_200_OK)
#---------------------------
class DeleteInformingProductAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        pk = request.data.get('id')

        if(not pk):
            return Response({'message': messages_for_front['not_id']}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        try:
            product = Product.objects.get(pk = pk)
        except:
            return Response({'message': messages_for_front['product_not_found']}, status=status.HTTP_404_NOT_FOUND)
    
        user.informing.remove(product)
        user.save()

        return Response({'message': messages_for_front['product_removed_from_informing']}, status=status.HTTP_200_OK)
#---------------------------
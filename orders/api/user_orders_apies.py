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
    The codes related to the site's user orders are in this app.
    api's in user_orders_apies.py :

    1- ListUserOrdersAPIView --> Lists all orders of user 


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
class ListUserOrdersAPIView(APIView):
    """Lists all orders of user """
    permission_classes = [IsAuthenticated]
    def get(self,request):
        orders = request.user.orders
        
        serializer = OrderDashBoardSerializer(orders, many=True)

        return Response({'data': serializer.data},status=status.HTTP_200_OK)
#---------------------------
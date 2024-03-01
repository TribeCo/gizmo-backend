import random
from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cart.models import Cart
from .serializers import *
from .models import User,Product,Comment,ProductComment
from blog.models import Article,ArticleComment
from inquiry.models import ForeignOrder
from orders.models import Order
from config.settings import SMS_PASSWORD,SMS_USERNAME
import requests
from products.serializers import ProductSerializer
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
    
}
#---------------------------
class UserCreateAPIView(APIView):
    """create a user"""
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': messages_for_front['user_created'], 'data': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class UserRetrieveAPIView(APIView):
    """ read one user with id """
    
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserReadSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': messages_for_front['user_not_found']}, status=status.HTTP_404_NOT_FOUND)
#---------------------------
class UserListAPIView(APIView):
    """read all user"""

    def get(self, request):
        users = User.objects.all()
        serializer = UserReadSerializer(users, many=True)
        return Response(serializer.data)
#---------------------------
class UserDeleteAPIView(APIView):
    """delete one user with id"""
    
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': messages_for_front['user_not_found']}, status=status.HTTP_404_NOT_FOUND)
#---------------------------
class UserUpdateAPIView(APIView):
    """update one user with id"""
    
    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserReadSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': messages_for_front['user_not_found']}, status=status.HTTP_404_NOT_FOUND)
#---------------------------
class CreateCommentForArticleAPIView(APIView):
    """create comment for article"""
    def post(self, request):
        serializer = ArticleCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class CreateCommentForProductAPIView(APIView):
    """create comment for product"""
    def post(self, request):
        serializer = ProductCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ReadCommentForProductAPIView(APIView):
    """read comment for a product"""
    def get(self, request, comment_id):
        try:
            comment = ProductComment.objects.get(id=comment_id)
        except ProductComment.DoesNotExist:
            return Response({'message': messages_for_front['comment_not_found']}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
#---------------------------
class ReadCommentForArticleAPIView(APIView):
    """read comment for a article"""
    def get(self, request, comment_id):
        try:
            comment = ArticleComment.objects.get(id=comment_id)
        except ArticleComment.DoesNotExist:
            return Response({'message': messages_for_front['comment_not_found']}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
#---------------------------
class DeleteCommentAPIView(APIView):
    """delete comment with id"""
    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'message': messages_for_front['comment_not_found']}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response({'message': messages_for_front['comment_deleted']}, status=status.HTTP_204_NO_CONTENT)
#---------------------------
class UpdateCommentAPIView(APIView):
    """update comment with id"""
    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'message': messages_for_front['comment_not_found']}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class CheckPhoneNumberAPIView(APIView):
    """This API checks whether the phone number is in the database or not"""
    def get(self, request,phone_number):
        try:
            user = User.objects.get(phoneNumber=phone_number)
        except User.DoesNotExist:
            return Response({'message': messages_for_front['user_not_found'],'in_database':'fasle'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': messages_for_front['user_found'],'in_database':'true'}, status=status.HTTP_200_OK)
#---------------------------
class CreateUserWithPhoneNumberAPIView(APIView):
    """Create user with phone number"""
    def post(self, request):
        text_sms = "name عزیز به گیزموشاپ خوش آمدید.\nکد احرازسنجی شما: code"
        link_sms = f"https://www.0098sms.com/sendsmslink.aspx?FROM=50002220096&TO=PhoneNumberUser&TEXT=TextCode&USERNAME={SMS_USERNAME}&PASSWORD={SMS_PASSWORD}&DOMAIN=0098"
        
        
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():      
            user = User(
                phoneNumber = serializer.validated_data['phoneNumber'],
                email = f"{serializer.validated_data['phoneNumber']}@gmail.com",
            )

            user.save()

            user.is_active = False
            code = random.randint(10000, 99999)
            user.code = code

            cart = Cart(user = user)
            cart.save()
            user.cart = cart

            user.save()

            # send code to user
            # text_sms = text_sms.replace("name" ,user.full_name)
            text_sms = text_sms.replace("code" , str(user.code))

            send_sms = link_sms.replace("PhoneNumberUser",user.phoneNumber)
            send_sms = send_sms.replace("TextCode",text_sms)

            # response = requests.get(send_sms)

            response_data = {
                'phoneNumber' : user.phoneNumber,
                'id' : user.id
            }
            

            return Response({'data' : response_data}, status=status.HTTP_201_CREATED)

            # if response.status_code == 200:
            #     return Response({'data' : response_data,'response_sms': response.json()}, status=status.HTTP_201_CREATED)
            # else:
            #     print('درخواست با خطا مواجه شد:', response.status_code)

            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class CheckCodeAPIView(APIView):
    """Sign up for frontend"""
    def post(self, request):

        code = request.data['code']
        phoneNumber = request.data['phoneNumber']

        if(not phoneNumber):
            return Response({'message': "users must have phoneNumber"}, status=status.HTTP_400_BAD_REQUEST)
        
        if(not code):
            return Response({'message': "users must have code"}, status=status.HTTP_400_BAD_REQUEST)

        try :
            user = User.objects.get(phoneNumber = phoneNumber)
        except User.DoesNotExist:
            return Response({'message': messages_for_front['user_not_found']}, status=status.HTTP_400_BAD_REQUEST)

        if(str(user.code) == str(code)):
            return Response({'message' : 'code is valid.'}, status=status.HTTP_200_OK)
        return Response({'message' : 'code is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

#---------------------------
class UpdateSignUpAPIView(APIView):
    """Sign up for frontend"""
    def post(self, request):

        phoneNumber = request.data['phoneNumber']
        email = request.data['email']
        full_name = request.data['full_name']
        password = request.data['password']


        if(not phoneNumber):
            return Response({'message': "users must have phoneNumber"}, status=status.HTTP_400_BAD_REQUEST)
        
        if(not email):
            return Response({'message': "users must have email"}, status=status.HTTP_400_BAD_REQUEST)
        
        if(not full_name):
            return Response({'message': "users must have full name"}, status=status.HTTP_400_BAD_REQUEST)

        if(not password):
            return Response({'message': "users must have password"}, status=status.HTTP_400_BAD_REQUEST)

        try :
            user = User.objects.get(email = email)
            return Response({'message': "use another email"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

        
        try :
            user = User.objects.get(phoneNumber = phoneNumber)
        except User.DoesNotExist:
            return Response({'message': messages_for_front['user_not_found']}, status=status.HTTP_400_BAD_REQUEST)

        if(user.is_active):
            return Response({'message': "can not update"}, status=status.HTTP_400_BAD_REQUEST)

        
        user.full_name = full_name
        user.email = email
        user.set_password(password)
        user.is_active = True
        code = random.randint(10000, 99999)
        user.code = code

        user.save()


        response_data = {
            'phoneNumber' : user.phoneNumber,
            'full_name' : user.full_name,
            'id' : user.id
        }       

        return Response({'data' : response_data}, status=status.HTTP_200_OK)
            
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class PasswordChangeRequest(APIView):
    def post(self, request):
        """
            Password change request
            urls : domain.com/..../users/update/password/
            Sample json :
            {
            "phoneNumber" : "09303615324",
            }

        """

        info = PasswordChangeRequestSerializer(data=request.data)
        

        if info.is_valid():
            try :
                user = User.objects.get(phoneNumber = info.validated_data['phoneNumber'])
            except User.DoesNotExist:
                return Response({'message': messages_for_front['user_not_found']}, status=status.HTTP_400_BAD_REQUEST)

            user.can_change_password = True
            code = random.randint(10000, 99999)
            user.code = code
            user.save()

            # send Code to User
            
            return Response({'message': messages_for_front['code_sent']}, status=status.HTTP_201_CREATED)
        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ChangePassword(APIView):
    """
            It change user password if can_change_password is active.
            urls : domain.com/..../users/change/password/
            Sample json :
            {
            "phoneNumber" : "09345454678",
            "password" : "338dsfs3fsaengh7",
            "code" : 76766
            }

    """
    def post(self, request):
        info = PasswordChangeSerializer(data=request.data)    

        if info.is_valid():
            try :
                user = User.objects.get(phoneNumber = info.validated_data['phoneNumber'])
            except User.DoesNotExist:
                return Response({'message': messages_for_front['user_not_found']}, status=status.HTTP_400_BAD_REQUEST)
            if (user.can_change_password):
                if(str(user.code) == str(info.validated_data['code'])):

                    user.set_password(info.validated_data.get('password'))
                    user.can_change_password = False
                    user.code = random.randint(10000, 99999)
                    user.save()

                    return Response({'message': messages_for_front['password_changed']}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': messages_for_front['wrong_coode']}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class CreateAddressAPIView(APIView):
    """create an address"""
    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ReadAddressAPIView(APIView):
    """read all addresses"""
    def get(self, request):
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)
#---------------------------
class UpdateAddressAPIView(APIView):
    """update address with id"""
    def put(self, request, pk):
        try:
            address = Address.objects.get(pk=pk)
            serializer = AddressSerializer(address, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Address.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
#---------------------------
class DeleteAddressAPIView(APIView):
    """delete address with id"""
    def delete(self, request, pk):
        try:
            address = Address.objects.get(pk=pk)
            address.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Address.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
#---------------------------
class FavoriteProductsAPIView(APIView):
    def get(self, request):        
        user = request.user        
        try:
            products = user.wishlist.all()
        except:
            return Response({'message': messages_for_front['favorite_products_not_found']}, status=status.HTTP_404_NOT_FOUND)
        

        favorite_products = ProductSerializer(products, many=True)
        return Response({'data': favorite_products.data})
#---------------------------
class AddFavoriteProductAPIView(APIView):
    def get(self, request, pk):
        user = request.user
        try:
            product = Product.objects.get(pk = pk)
        except:
            return Response({'message': 'محصول مورد نظر وجود ندارد'}, status=status.HTTP_404_NOT_FOUND)
        
        user.wishlist.add(product)
        user.save()

        return Response({'message': messages_for_front['product_added_to_wishlist']},status=status.HTTP_200_OK)
#---------------------------
class DeleteFvaoriteProductAPIView(APIView):
    def delete(self, request, pk):
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
    def get(self, request):
        if request.user.is_authenticated:
            orders_count = Order.objects.filter(user=request.user).count()
            returns_count = Order.objects.filter(user=request.user, returned=True).count()
            foreign_returns_count = ForeignOrder.objects.filter(user=request.user).count()
            return Response({'orders_count': orders_count, 'returns_count': returns_count, 'foreign_returns_count': foreign_returns_count}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


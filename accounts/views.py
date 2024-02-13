import random
from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer,UserReadSerializer,ArticleCommentSerializer,ProductCommentSerializer,CommentSerializer
from .models import User,Article,Product,Comment,ProductComment,ArticleComment
from config.settings import SMS_PASSWORD,SMS_USERNAME
import requests
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

"""
#---------------------------
messages_for_front = {
    'user_created' : 'کاربر جدید ایجاد شد.',
    'user_not_found' : 'کاربر یافت نشد',
    'article_not_found' : 'مقاله یافت نشد',
    'product_not_found' : 'محصول یافت نشد',
    'comment_not_found' : 'نظر یافت نشد',
    'comment_deleted' : 'نظر حذف شد'
    
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
class SignUpAPIView(APIView):
    """Sign up for frontend"""
    def post(self, request):
        text_sms = "name عزیز به گیزموشاپ خوش آمدید.\nکد احرازسنجی شما: code"
        link_sms = f"https://www.0098sms.com/sendsmslink.aspx?FROM=50002220096&TO=PhoneNumberUser&TEXT=TextCode&USERNAME={SMS_USERNAME}&PASSWORD={SMS_PASSWORD}&DOMAIN=0098"
        
        
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():

            if(not serializer.validated_data.get('full_name')):
                return Response({'message': "users must have full name"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User(
                phoneNumber = serializer.validated_data['phoneNumber'],
                email = serializer.validated_data['email'],
                full_name = serializer.validated_data['full_name'],
            )

            user.set_password(serializer.validated_data['password'])
            user.is_active = False
            code = random.randint(10000, 99999)
            user.code = code

            user.save()

            # send code to user
            text_sms = text_sms.replace("name" ,user.full_name)
            text_sms = text_sms.replace("code" , str(user.code))

            send_sms = link_sms.replace("PhoneNumberUser",user.phoneNumber)
            send_sms = send_sms.replace("TextCode",text_sms)

            # response = requests.get(send_sms)

            response_data = {
                'phoneNumber' : user.phoneNumber,
                'full_name' : user.full_name,
                'id' : user.id
            }
            

            return Response({'data' : response_data}, status=status.HTTP_201_CREATED)

            # if response.status_code == 200:
            #     return Response({'data' : response_data,'response_sms': response.json()}, status=status.HTTP_201_CREATED)
            # else:
            #     print('درخواست با خطا مواجه شد:', response.status_code)

            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


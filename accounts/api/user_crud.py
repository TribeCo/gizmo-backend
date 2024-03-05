from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import User
from rest_framework.permissions import IsAuthenticated
#---------------------------
"""
    The codes related to the site's user cruds are in this app.
    api's in user_crud.py :

    1- UserCreateAPIView --> create a user
    2- UserRetrieveAPIView --> read one user with id
    3- UserListAPIView --> read all user
    4- UserDeleteAPIView --> delete one user with id
    5- UserUpdateAPIView --> update one user with id

"""
#---------------------------
messages_for_front = {
    'user_created' : 'کاربر جدید ایجاد شد.',
    'user_not_found' : 'کاربر یافت نشد',
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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    """read all user"""

    def get(self, request):
        users = User.objects.all()
        serializer = UserReadSerializer(users, many=True)
        return Response(serializer.data)
#---------------------------
class UserDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
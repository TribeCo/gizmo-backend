from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
#---------------------------
"""
    The codes related to the Dubai Order.
    api's in api_views.py :

    1- BrandCreateAPIView --> create a brand
    

"""
#---------------------------
messages_for_front = {
    'foreign_order_created' : 'سفارش جدید ساخته شد.',
    }
#---------------------------
class CreateForeignOrder(APIView):
    def post(self,request):
        serializer = ForeignOrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response({'message' : messages_for_front['foreign_order_created']},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#---------------------------
        
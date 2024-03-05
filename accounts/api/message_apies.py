
from itertools import product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import WatchedProduct

from products.models import Product
from ..serializers import *
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
#---------------------------
"""
    The codes related to the site's user Message are in this app.
    api's in message_apies.py :

    1- CreateMessageAPIView --> create an message
    2- ReadMessageAPIView --> read all messages
    3- UpdateMessageAPIView --> update message with id
    4- DeleteMessageAPIView --> delete message with id

"""
#---------------------------
messages_for_front = {
    'message_created' : 'آدرس جدید ذخیره شد.',
    'product_not_found' : 'محصول مورد نظر وجود ندارد',
}
#---------------------------
class CreateMessageAPIView(APIView):
    """create an message"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = MessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'messages':messages_for_front['message_created'],'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ReadMessageAPIView(RetrieveAPIView):
    """Getting the information of a Brand with ID"""
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    lookup_field = 'pk'
#---------------------------
class UpdateMessageAPIView(UpdateAPIView):
    """update message with id"""
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageCreateSerializer
    lookup_field = 'pk'
#---------------------------
class DeleteMessageAPIView(DestroyAPIView):
    """delete message with id"""
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    lookup_field = 'pk'
#---------------------------
class UserMessageAPIView(APIView):
    """get an user messagees"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = MessageSerializer(request.user.messages,many=True)
        return Response({'data':serializer.data,}, status=status.HTTP_201_CREATED)
#---------------------------
# class ProductMessageAPIView(APIView):
#     """send messages to users for availble product"""
#     permission_classes = [IsAuthenticated]
#     def get(self, request,pk):
#         try:
#             product = Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             return Response({'messages':messages_for_front['product_not_found' ]}, status=status.HTTP_404_NOT_FOUND)
        
#         watch_products = WatchedProduct.object.filter(product=product)
#         for wp in watch_products:

#         serializer = MessageSerializer(request.user.messages,many=True)
#         return Response({'data':serializer.data,}, status=status.HTTP_201_CREATED)
#---------------------------


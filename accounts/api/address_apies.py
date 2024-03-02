
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
#---------------------------
"""
    The codes related to the site's user Address are in this app.
    api's in address_apies.py :

    1- CreateAddressAPIView --> create an address
    2- ReadAddressAPIView --> read all addresses
    3- UpdateAddressAPIView --> update address with id
    4- DeleteAddressAPIView --> delete address with id

"""
#---------------------------
messages_for_front = {
    'address_created' : 'آدرس جدید ذخیره شد.',
}
#---------------------------
class CreateAddressAPIView(APIView):
    """create an address"""
    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'messages':messages_for_front['address_created'],'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ReadAddressAPIView(RetrieveAPIView):
    """Getting the information of a Brand with ID"""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'pk'
#---------------------------
class UpdateAddressAPIView(UpdateAPIView):
    """update address with id"""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'pk'
#---------------------------
class DeleteAddressAPIView(DestroyAPIView):
    """delete address with id"""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'pk'
#---------------------------
class UserAddressAPIView(APIView):
    """get an user addresses"""
    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'messages':messages_for_front['address_created'],'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


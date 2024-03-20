
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
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
    'address_not_found' : 'آدرس یافت نشد.',
    'address_changed' : 'آدرس با موفقیت تغییر کرد.',
    'not_id' : 'آیدی مورد نیاز است.',
    'tomany_address' : 'تعداد آدرس های ذخیره شده زیاد است.',
}
#---------------------------
class CreateAddressAPIView(APIView):
    """create an address"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if(request.user.addresses.count() > 2):
            return Response({'messages':messages_for_front['tomany_address']}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save(user=request.user,phone_number=request.user.phoneNumber)
            return Response({'messages':messages_for_front['address_created'],'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ReadAddressAPIView(RetrieveAPIView):
    """Getting the information of a Address with ID"""
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'pk'
#---------------------------
class ReadUserAddressAPIView(ListAPIView):
    """Getting the information of a Address with ID"""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        addresses = request.user.addresses.all()
        serializer = AddressSerializer(addresses,many=True)
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)
#---------------------------
class UpdateAddressAPIView(UpdateAPIView):
    """update address with id"""
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'pk'
#---------------------------
class DeleteAddressAPIView(DestroyAPIView):
    """delete address with id"""
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'pk'
#---------------------------
class UserAddressAPIView(APIView):
    """get an user addresses"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'messages':messages_for_front['address_created'],'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class SetUserAddressAPIView(APIView):
    """ser an user addresses"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        pk = request.data.get('id')

        if(not pk):
            return Response({'message': messages_for_front['not_id']}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        try:
            address = user.addresses.get(pk = pk)
        except Address.DoesNotExist:
            return Response({'message': messages_for_front['address_not_found']}, status=status.HTTP_404_NOT_FOUND)
        
        user.change_current_address(address.id)

        return Response({'messages':messages_for_front['address_changed']}, status=status.HTTP_200_OK)
#---------------------------


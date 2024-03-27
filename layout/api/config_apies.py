from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from ..serializers import *
from ..models import Config
#---------------------------
"""
    The codes related to the shop's config are in this app.
    api's in config_apies.py :

    1- ConfigCreateAPIView --> create a config
    2- ConfigAllListAPIView --> List of all config
    3- ConfigDetailView  --> Getting the information of a config with ID

"""
#---------------------------
messages_for_front = {
    'config_created' : 'کانفیگ جدید ساخته شد.',
    }
#---------------------------
# class ConfigCreateAPIView(APIView):
#     """
#         create a config
#     """
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         serializer = ConfigSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': messages_for_front['config_created'],'data' : serializer.data}, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ConfigForAboutUsAPIView(APIView):
    """get config Shop"""
    def get(self, request):
        config = Config.objects.get(current=True)
        serializer = ConfigForAboutUsSerializer(config)

        return Response({'data' : serializer.data}, status=status.HTTP_200_OK)
#---------------------------
class ConfigForEnamadAPIView(APIView):
    """get config Shop"""
    def get(self, request):
        config = Config.objects.get(current=True)
        serializer = ConfigForEnamadSerializer(config)

        return Response({'data' : serializer.data}, status=status.HTTP_200_OK)
#---------------------------


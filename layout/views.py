from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Banner
from .serializers import BannerSerializer
#---------------------------
"""
    The codes related to the site's products are in this app.
    api's in api_views.py :

    1- CreateBannerAPIView --> create a banner
    2- ReadBannerBySlugAPIView --> read banner api with for what input
    3- DeleteBannerAPIView --> delete banner with id
    4- UpdateBannerAPIView --> update banner with id

"""
#---------------------------
messages_for_front = {
    'banner_created' : 'بنر جدید ایجاد شد',
    'banner_not_found' : 'بنر یافت نشد',
    'banner_deleted' : 'بنر حذف شد',
    
}
#---------------------------
class CreateBannerAPIView(APIView):
    """Create a new banner"""
    def post(self, request):
        serializer = BannerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': messages_for_front['banner_created'],'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ReadBannerBySlugAPIView(APIView):
    """Read a banner by slug"""
    def get(self, request, slug):
        try:
            banner = Banner.objects.get(for_what=slug)
            serializer = BannerSerializer(banner)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Banner.DoesNotExist:
            return Response({'message': messages_for_front['banner_not_found']}, status=status.HTTP_404_NOT_FOUND)
#---------------------------
class DeleteBannerAPIView(APIView):
    """Delete a banner with a given ID"""
    def delete(self, request, banner_id):
        try:
            banner = Banner.objects.get(id=banner_id)
            banner.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Banner.DoesNotExist:
            return Response({'message': messages_for_front['banner_not_found']}, status=status.HTTP_404_NOT_FOUND)
#---------------------------
class UpdateBannerAPIView(APIView):
    """Update a banner with a given ID"""
    def put(self, request, banner_id):
        try:
            banner = Banner.objects.get(id=banner_id)
        except Banner.DoesNotExist:
            return Response({'message': messages_for_front['banner_not_found']}, status=status.HTTP_404_NOT_FOUND)

        serializer = BannerSerializer(banner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

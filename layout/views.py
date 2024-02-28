from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Banner,FAQGroup,FAQ,Picture
from .serializers import BannerSerializer,FAQGroupSerializer,FAQSerializer,PictureSerializer
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
#---------------------------
"""
    The codes related to the site's products are in this app.
    api's in api_views.py :

    1- CreateBannerAPIView --> create a banner
    2- ReadBannerBySlugAPIView --> read banner api with for what input
    3- DeleteBannerAPIView --> delete banner with id
    4- UpdateBannerAPIView --> update banner with id
    6- CreateFAQGroupAPIView --> create a new FAQ group
    7- ReadFAQGroupAPIView --> read all FAQ groups
    8- UpdateFAQGroupAPIView --> update an existing FAQ group
    9- DeleteFAQGroupAPIView --> delete an existing FAQ group
    10- CreateFAQAPIView --> creae a new FAQ
    11- ReadFAQAPIView --> read all FAQs
    12- UpdateFAQAPIView --> update an existing FAQ
    13- DeleteFAQAPIView --> delete an existing FAQ
    

"""
#---------------------------
messages_for_front = {
    'banner_created' : 'بنر جدید ایجاد شد',
    'banner_not_found' : 'بنر یافت نشد',
    'picture_created' : 'تصویر با موفقیت ذخیره شد.',
    'banner_deleted' : 'بنر حذف شد',
    
}
#---------------------------
class CreateBannerAPIView(APIView):
    """
    Create a new banner
    
    "bigTitle": 
    "smallTitle": 
    "image": 
    "for_what": 
    "main_link": 
    "out_link": 
    
    """
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
#---------------------------
class PictureCreateAPIView(APIView):
    """
        create a Picture objects with post method.
        {
            "name": "login page background",
            "image" 
        }
    """
    def post(self, request):
        serializer = PictureSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': messages_for_front['picture_created'],'data' : serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class PictureAllListAPIView(ListAPIView):
    """List of all Pictures"""
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
#---------------------------
class PictureDetailView(RetrieveAPIView):
    """Getting the information of a Picture with ID(domain.com/..../pk/)"""
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    lookup_field = 'pk'
#---------------------------
class PictureDeleteView(DestroyAPIView):
    """Remove a Picture with an ID(domain.com/..../pk/)"""
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    lookup_field = 'pk'
#---------------------------
class PictureUpdateView(UpdateAPIView):
    """Update Picture information with ID(domain.com/..../pk/)"""
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    lookup_field = 'pk'  
#---------------------------   
class CreateFAQGroupAPIView(APIView):
    """
     creating a new FAQ group
     
     "title":
     
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = FAQGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#--------------------------- 
class ReadFAQGroupAPIView(APIView):
    """
     read all FAQ groups
    """
    def get(self, request):
        faq_groups = FAQGroup.objects.all()
        serializer = FAQGroupSerializer(faq_groups, many=True)
        return Response(serializer.data)
#--------------------------- 
class UpdateFAQGroupAPIView(APIView):
    """
     update an existing FAQ group
    """
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        try:
            faq_group = FAQGroup.objects.get(pk=pk)
            serializer = FAQGroupSerializer(faq_group, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except FAQGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
#--------------------------- 
class DeleteFAQGroupAPIView(APIView):
    """
     delete an existing FAQ group
    """
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            faq_group = FAQGroup.objects.get(pk=pk)
            faq_group.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FAQGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
#--------------------------- 
class CreateFAQAPIView(APIView):
    """
     creae a new FAQ
     
     "group": 
    "question": 
    "answer":
    
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = FAQSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#--------------------------- 
class ReadFAQAPIView(APIView):
    """
     read all FAQs
    """
    def get(self, request):
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data)
#--------------------------- 
class UpdateFAQAPIView(APIView):
    """
      update an existing FAQ
    """
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        try:
            faq = FAQ.objects.get(pk=pk)
            serializer = FAQSerializer(faq, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except FAQ.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
#--------------------------- 
class DeleteFAQAPIView(APIView):
    """
     delete an existing FAQ
    """
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            faq = FAQ.objects.get(pk=pk)
            faq.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FAQ.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
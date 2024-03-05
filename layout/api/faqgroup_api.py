from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from layout.models import FAQGroup
from layout.serializers import FAQGroupSerializer
from rest_framework.permissions import IsAuthenticated
#---------------------------
"""
    The codes related to the site's products are in this app.
    api's in api_views.py :

    1- CreateFAQGroupAPIView --> create a new FAQ group
    2- ReadFAQGroupAPIView --> read all FAQ groups
    3- UpdateFAQGroupAPIView --> update an existing FAQ group
    4- DeleteFAQGroupAPIView --> delete an existing FAQ group

"""
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
    def delete(self, request, pk):
        try:
            faq_group = FAQGroup.objects.get(pk=pk)
            faq_group.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FAQGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
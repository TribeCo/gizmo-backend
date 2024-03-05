from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from layout.models import FAQ
from layout.serializers import FAQSerializer
from rest_framework.permissions import IsAuthenticated
#---------------------------
"""
    The codes related to the site's products are in this app.
    api's in api_views.py :

    1- CreateFAQAPIView --> creae a new FAQ
    2- ReadFAQAPIView --> read all FAQs
    3- UpdateFAQAPIView --> update an existing FAQ
    4- DeleteFAQAPIView --> delete an existing FAQ
    
"""
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
    def delete(self, request, pk):
        try:
            faq = FAQ.objects.get(pk=pk)
            faq.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FAQ.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
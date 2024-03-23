from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from inquiry.serializers import *
#---------------------------
"""
    The codes related to the site's products are in this app.
    api's in api_views.py :

    1- DubaiSitesCreateAPIView --> create a other sites
    2- DubaiSitesAllListAPIView --> List of all other sites
    3- DubaiSitesDetailView  --> Getting the information of a other sites with ID
    4- DubaiSitesDeleteView --> Remove a other sites with an ID
    5- DubaiSitesUpdateView --> Update other sites information with ID

"""
#---------------------------
messages_for_front = {
    'other_sites_created' : 'برند جدید ساخته شد.',
    }
#---------------------------
class ForeignProductCreateAPIView(APIView):
    """
    Create a Product
    """
    def post(self, request):    
        serializer = ForeignProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': messages_for_front['product_created']})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
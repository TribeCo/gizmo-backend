from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from layout.models import Picture
from layout.serializers import PictureSerializer
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
#---------------------------

"""
    The codes related to the site's products are in this app.
    api's in api_views.py :

    1- PictureCreateAPIView --> create a Picture objects with post method
    2- PictureAllListAPIView --> List of all Pictures
    3- PictureDetailView --> Getting the information of a Picture with ID
    4- PictureDeleteView --> Remove a Picture with an ID
    5- PictureUpdateView --> Update Picture information with ID
    

"""
#---------------------------
messages_for_front = {
    
    'picture_created' : 'تصویر با موفقیت ذخیره شد.',
    
}
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
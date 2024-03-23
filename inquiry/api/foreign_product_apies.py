from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from inquiry.serializers import *
import requests
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
    'dubai_site_not_found' : 'سایت پیدا نشد.',
    }
#---------------------------
import os
class ForeignProductCreateAPIView(APIView):
    """Create a Product"""
    def post(self, request):    
        serializer = LinkSerializer(data=request.data)
        
        
        if serializer.is_valid():
            url = 'https://scrapt.liara.run/server/scraper/'
            data = {"url": request.data.get('url'),}

            response = requests.post(url, data=data)
            data_res = response.json()
            print(data_res)


            try:
                website = DubaiSites.objects.get(name = data_res['data']['site'])
            except DubaiSites.DoesNotExist:
                return Response({'message': messages_for_front['dubai_site_not_found']})

            image_url = data_res['data']['image']
            image_response = requests.get(image_url)
            image_extension = os.path.splitext(image_url)[1]
            image_path = os.path.join('data/', 'image_name' + image_extension)

            # Save the image locally
            with open(image_path, 'wb') as f:
                f.write(image_response.content)
                
            product = ForeignProduct(name = data_res['data']['name'],image1=image_path,
            website=website,
            )
            discount=data_res['data']['discount']
            if(discount) :
                product.discount = True
                product.price = int(float(data_res['data']['price_out']))
            else:
                product.discount = False
                product.price = int(float(data_res['data']['price']))
            product.save()
            return Response({'message': 'ok'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from inquiry.serializers import *
import requests
import random 
import string
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
            data_res = response.json()['data']
            print(data_res)
            



            name = data_res['name']
            site = data_res['site']
            discount = data_res['discount']
            image_url = data_res['image']
            url = data_res['url']

            try:
                website = DubaiSites.objects.get(name = site)
            except DubaiSites.DoesNotExist:
                return Response({'message': messages_for_front['dubai_site_not_found']})
            
            text = data_res['name'][0:10]
            text = text.replace(" ","-")
            slug = f"{website.name}-{text}-{''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))}"

            # random_name = f"{website.name}-{data_res['name'][0:10]}-{''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))}"
            # image_response = requests.get(image_url)
            # image_extension = os.path.splitext(image_url)[1]
            # image_path = os.path.join('data/', random_name + image_extension)

            # Save the image locally
            # with open(image_path, 'wb') as f:
            #     f.write(image_response.content)
                
            product = ForeignProduct(name = name,image_link=image_url,
            website=website,slug= slug,product_url=url
            )
            
            
            if(discount) :
                product.discounted = True

                string_price = data_res['price_out']
                string_price = string_price.replace(",","")

                string_price_in = data_res['price_in']
                string_price_in = string_price_in.replace(",","")

                price = int(float(string_price))
                if(float(string_price) - price > 0):
                    price += 1

                price_in = int(float(string_price_in))
                if(float(string_price_in) - price_in > 0):
                    price_in += 1

                discount_amount = 100 * (price - price_in) / price 

                

                product.price = price
                product.discount = discount_amount
            else:
                product.discount = False

                string_price = data_res['price']
                string_price = string_price.replace(",","")

                price = int(float(string_price))
                if(float(string_price) - price > 0):
                    price += 1

                product.price = price


            product.save()


            return Response({'message': 'ok'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------

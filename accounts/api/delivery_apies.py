from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cart.models import Cart
from ..serializers import *
from ..models import User
from config.settings import SMS_PASSWORD,SMS_USERNAME
import random
from rest_framework.permissions import IsAuthenticated
#---------------------------
"""
    The codes related to the site's user model are in this app.
    api's in delivery_apies.py:

    1- UpdateInfoDelivery --> It update info of Delivery for orders.
    
"""
#---------------------------
messages_for_front = {
    'delivery_updated' : 'اطلاعات ذخیره شد.',
}
#---------------------------
class UpdateInfoDelivery(APIView):
    """
            It update info of Delivery for orders.
            urls : domain.com/..../users/update/delivery/
            Sample json :
            {
                "name_delivery": "taha mousavi",
                "description": "tozihat",
                "delivery_method": "tozihat",
                "phone_delivery": "021557438345"
            }

    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        info = DeliveryInfoSerializer(data=request.data)    
        user = request.user
        if info.is_valid():
            if(user.delivery_info):
                user.delivery_info.delete()
            info.save()
            user.delivery_info = info.instance
            user.save()
            return Response({'messages':messages_for_front['delivery_updated'],'data':info.data}, status=status.HTTP_202_ACCEPTED)
            
        else:
            return Response(info.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
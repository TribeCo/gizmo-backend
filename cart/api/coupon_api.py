from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
#---------------------------
"""
    The codes related to the site's coupon are in this app.
    api's in coupon_api.py :

    1- CouponCreateAPIView --> create a Coupon
    2- CouponAllListAPIView --> List of all Coupon
    3- CouponDetailView --> Getting the information of a Coupon with ID
    4- CouponDeleteView --> Remove a Coupon with an ID

    5- CouponUpdateView --> Update Coupon information with ID
    6- ApplyCouponToCartAPIView --> Apply coupon to cart
"""
#---------------------------
messages_for_front = {
    'coupon_created' : 'کد تخفیف جدید ایجاد شد.',
    'coupon_updated' : 'کد تخفیف آپدیت شد.',
    'coupon_deleted' : 'کد تخفیف حذف شد.',
    'coupon_not_found' : 'کد تخفیف یافت نشد.',
    'coupon_is_not_valid' : 'کد تخفیف معتبر نیست.',
    'coupon_applied' : 'کد تخفیف با موفقیت اعمال شد.',
}
#---------------------------
class CouponCreateAPIView(APIView):
    """
        create a Coupon
        {
            "code": "Asus",
            "valid_from": ,
            "valid_to": ,
            "discount": 20
        }
    """
    serializer_class = CouponSerializer
    def post(self, request):
        serializer = CouponSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': messages_for_front['coupon_created'],'data' : serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class CouponAllListAPIView(ListAPIView):
    """List of all Coupon"""
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
#---------------------------
class CouponDetailView(RetrieveAPIView):
    """Getting the information of a Coupon with ID(domain.com/..../pk/)"""
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    lookup_field = 'pk'
#---------------------------
class CouponDeleteView(DestroyAPIView):
    """Remove a Coupon with an ID(domain.com/..../pk/)"""
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    lookup_field = 'pk'
#---------------------------
class CouponUpdateView(UpdateAPIView):
    """Update Coupon information with ID(domain.com/..../pk/)"""
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    lookup_field = 'pk'
#---------------------------
class ApplyCouponToCartAPIView(APIView):
    """Apply coupon to cart"""
    def post(self, request,pk):

        try:
            coupon = Coupon.objects.get(id=pk)
        except Coupon.DoesNotExist:
            return Response({'message':messages_for_front['coupon_not_found']}, status=status.HTTP_404_NOT_FOUND)

        cart = request.user.cart


        if coupon.is_valid():
            
            cart.discount = coupon.discount
            cart.save()
            return Response({'message':messages_for_front['coupon_applied']}, status=status.HTTP_201_CREATED)
        
        return Response({'message':messages_for_front['coupon_is_not_valid']}, status=status.HTTP_400_BAD_REQUEST)  
#---------------------------
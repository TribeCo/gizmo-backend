from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from ..serializers import *
#---------------------------
"""
    The codes related to the Dubai Order.
    api's in api_views.py :

    1- ForeignOrderCreateAPIView --> create a ForeignOrder
    2- ForeignOrderAllListAPIView --> List of all Foreign Orders
    3- ForeignOrderDetailView --> Getting the information of a Foreign Order with ID
    4- ForeignOrderDeleteView --> Remove a Foreign Order with an ID
    5- ForeignOrderUpdateView --> Update Foreign Order information with ID
    

"""
#---------------------------
messages_for_front = {
    'foreign_order_created' : 'سفارش جدید ساخته شد.',
    'foreign_order_deleted' : 'سفارش حذف شد',
    'foreign_order_updated' : 'سفارش آپدیت شد.',
    'product_not_found' : 'محصول یافت نشد.',
    }
#---------------------------
class CreateForeignOrder(APIView):
    """create a ForeignOrder"""
    serializer_class = ForeignOrderSerializer
    permission_classes = [IsAuthenticated]
    def post(self,request):
        pk = request.data.get('id')

        try:
            product = ForeignProduct.objects.get(id=pk)
        except ForeignProduct.DoesNotExist:
            return Response({'message': messages_for_front['product_not_found']}, status=status.HTTP_404_NOT_FOUND)

        order_product = ForeignOrder(user=request.user,
        link=product.product_url,price=product.price,
        discounted=product.discounted,discounted_price=product.discounted_price_int,
        product=product,name=product.name,
        image=product.image_link)

        order_product.save()

        info = ForeignOrderSerializer(order_product)

        return Response({'message' : messages_for_front['foreign_order_created'],'data':info.data},status=status.HTTP_201_CREATED)     
#---------------------------
class ForeignOrderAllListAPIView(ListAPIView):
    """List of all Foreign Orders"""
    permission_classes = [IsAuthenticated]
    queryset = ForeignOrder.objects.all()
    serializer_class = ForeignOrderSerializer
#---------------------------
class ForeignOrderUserListAPIView(APIView):
    """get user Foreign Orders"""
    serializer_class = ForeignOrderSerializer
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user

        orders = user.foreign_orders.all()
        

        info = ForeignOrderSerializer(orders,many=True)

        return Response({'data':info.data,},status=status.HTTP_201_CREATED)     
#---------------------------
class ForeignOrderDetailView(RetrieveAPIView):
    """Getting the information of a Foreign Order with ID(domain.com/..../pk/)"""
    queryset = ForeignOrder.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ForeignOrderSerializer
#---------------------------
class ForeignOrderDeleteView(DestroyAPIView):
    """Remove a Foreign Order with an ID(domain.com/..../pk/)"""
    queryset = ForeignOrder.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ForeignOrderSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": messages_for_front['foreign_order_deleted']}, status=status.HTTP_204_NO_CONTENT)
#---------------------------
class ForeignOrderUpdateView(UpdateAPIView):
    """Update Foreign Order information with ID(domain.com/..../pk/)"""
    queryset = ForeignOrder.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ForeignOrderSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": messages_for_front['foreign_order_updated']}, status=status.HTTP_200_OK)
#---------------------------         
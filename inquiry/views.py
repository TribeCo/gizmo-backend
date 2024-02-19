from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
#---------------------------
"""
    The codes related to the Dubai Order.
    api's in api_views.py :

    1- ForeignOrderCreateAPIView --> create a ForeignOrder
    

"""
#---------------------------
messages_for_front = {
    'foreign_order_created' : 'سفارش جدید ساخته شد.',
    'foreign_order_deleted' : 'سفارش حذف شد',
    'foreign_order_updated' : 'سفارش آپدیت شد.',
    }
#---------------------------
class CreateForeignOrder(APIView):
    def post(self,request):
        serializer = ForeignOrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response({'message' : messages_for_front['foreign_order_created']},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ForeignOrderAllListAPIView(ListAPIView):
    """List of all Foreign Orders"""
    queryset = ForeignOrder.objects.all()
    serializer_class = ForeignOrderSerializer
#---------------------------
class ForeignOrderDetailView(RetrieveAPIView):
    """Getting the information of a Foreign Order with ID(domain.com/..../pk/)"""
    queryset = ForeignOrder.objects.all()
    serializer_class = ForeignOrderSerializer
#---------------------------
class ForeignOrderDeleteView(DestroyAPIView):
    """Remove a Foreign Order with an ID(domain.com/..../pk/)"""
    queryset = ForeignOrder.objects.all()
    serializer_class = ForeignOrderSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": messages_for_front['foreign_order_deleted']}, status=status.HTTP_204_NO_CONTENT)
#---------------------------
class ForeignOrderUpdateView(UpdateAPIView):
    """Update Foreign Order information with ID(domain.com/..../pk/)"""
    queryset = ForeignOrder.objects.all()
    serializer_class = ForeignOrderSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": messages_for_front['foreign_order_updated']}, status=status.HTTP_200_OK)
#---------------------------         
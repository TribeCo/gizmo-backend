from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from ..serializers import TicketSerializer
from ..models import Ticket
#---------------------------
"""
    The codes related to the site's products are in this app.
    api's in ticket_apies.py :

    1- TicketCreateAPIView --> create a ticket
    2- TicketAllListAPIView --> List of all ticket
    3- TicketDetailView  --> Getting the information of a ticket with ID

"""
#---------------------------
messages_for_front = {
    'ticket_created' : 'تیکت جدید ساخته شد.',
    }
#---------------------------
class TicketCreateAPIView(APIView):
    """
        create a ticket
        {
            "name": "ali",
            "email": "ali@gmail.com",
            "phoneNumber": "09303016476",
            "title": "about ticket.",
            "text": "text."
        }
    """
    
    def post(self, request):
        serializer = TicketSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': messages_for_front['ticket_created'],'data' : serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class TicketAllListAPIView(ListAPIView):
    """List of all Tickets"""
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
#---------------------------
class TicketDetailView(RetrieveAPIView):
    """Getting the information of a Ticket with ID(domain.com/..../pk/)"""
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'pk'
#---------------------------


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from layout.models import Rule
from layout.serializers import RuleSerializer
#---------------------------
messages_for_front = {
    'rule_not_found' : 'قانون پیدا نشد ',
}
#---------------------------
class RuleAPIView(APIView):
    """ return rule """
    def get(self, request):
        rules = Rule.objects.all()
        serializer = RuleSerializer(rules,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#--------------------------- 
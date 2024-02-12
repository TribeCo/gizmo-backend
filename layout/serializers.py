from rest_framework import serializers
from .models import banner
#---------------------------
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = banner
        fields = '__all__'
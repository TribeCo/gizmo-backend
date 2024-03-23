from rest_framework import serializers
import requests
from .models import *
#---------------------------
class ForeignOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignOrder
        fields = ['name','link','price','discounted','discounted_price','image','admin_checked','profit']
#---------------------------
class DubaiSitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DubaiSites
        fields = ['name','website','logo']
#---------------------------
class ForeignProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignProduct
        fields = '__all__'
#---------------------------
class LinkSerializer(serializers.Serializer):
    url = serializers.URLField()

    def validate_url(self, value):
        response = requests.get(value)
        if response.status_code != 200:
            raise serializers.ValidationError("Cannot access the provided URL")
        return value
#---------------------------

from rest_framework import serializers
import requests
from .models import *
#---------------------------
class ForeignOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignOrder
        fields = ['tracking_code','name','website_name','link','shamsi_date','toman_price','toman_total','admin_checked']
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

    # def validate_url(self, value):
    #     response = requests.get(value)
    #     if response.status_code != 200:
    #         raise serializers.ValidationError("Cannot access the provided URL")
    #     return value
#---------------------------
class DubaiProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.CharField(source='discounted_price_int')

    class Meta:
        model = ForeignProduct
        fields = ['id','name','image_link','price','discounted','discounted_price','discount','product_url']
#---------------------------

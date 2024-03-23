from rest_framework import serializers
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
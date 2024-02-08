from rest_framework import serializers
from .models import *
#---------------------------
class BrandSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField()
    class Meta:
        model = Brand
        fields = ('name', 'slug', 'logo', 'description',)
#---------------------------
#---------------------------
#---------------------------
#---------------------------
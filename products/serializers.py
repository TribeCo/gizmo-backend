from rest_framework import serializers
from .models import *
#---------------------------
class BrandSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField()
    class Meta:
        model = Brand
        fields = ('name', 'slug', 'logo', 'description','id')
#---------------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
#---------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
#---------------------------
#---------------------------
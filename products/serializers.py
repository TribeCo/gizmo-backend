from unicodedata import category
from rest_framework import serializers
from .models import *
#---------------------------
class BrandSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField()
    class Meta:
        model = Brand
        fields = ('name', 'slug', 'logo', 'description','id')
#---------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
#---------------------------
class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'
#---------------------------
class CategoryLandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','image','slug']
#---------------------------
class ProductSliderSerializer(serializers.ModelSerializer):
    discounted_price = serializers.CharField(source='discounted_price_int')
    class Meta:
        model = Product
        fields = ['name','image','price','discounted','discounted_price','discount','is_new']
#---------------------------
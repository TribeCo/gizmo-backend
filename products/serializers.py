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
class CategoryProductPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','slug',]
#---------------------------
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields =  '__all__'
#---------------------------
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields =  '__all__'
#---------------------------
class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategoryProductPageSerializer(many=True)
    colors = ColorSerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'
#---------------------------
from django.utils.html import strip_tags

class ProductPageSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategoryProductPageSerializer(many=True)
    colors = ColorSerializer(many=True)
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ["id","brand","category","colors","images" ,"content","En","slug","price","image","alt","available","created","updated","rating","warehouse",
        "short_description","description","more_info","ordered","send_free","net_sale","code","discount","discounted"]
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['content'] = strip_tags(instance.content)
        return data
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
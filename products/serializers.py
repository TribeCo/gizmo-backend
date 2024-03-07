from unicodedata import category
from rest_framework import serializers
from django.utils.html import strip_tags
from .models import *
from config.settings import DOMAIN
#---------------------------
class BrandSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField()
    class Meta:
        model = Brand
        fields = ('name', 'slug', 'logo', 'description','id','website')
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
class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields =  ['key','value','is_main']
#---------------------------
class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategoryProductPageSerializer(many=True)
    colors = ColorSerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'
#---------------------------
class ProductPageSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategoryProductPageSerializer(many=True)
    colors = ColorSerializer(many=True)
    images = ProductImageSerializer(many=True)
    attributes = AttributeSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id','attributes','brand','category','colors','images' ,'content','En','slug','price','image1','image2','alt','available',
        'created','updated','rating','warehouse','ordered','send_free','net_sale','code','discount','discounted']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['content'] = strip_tags(instance.content)
        return data
#---------------------------
class CategoryLandingSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, obj):
        image_url = '{}{}'.format(DOMAIN, obj.image.url) if obj.image else None
        return image_url

    class Meta:
        model = Category
        fields = ['id','name','image','slug','color']
#---------------------------
class ProductSliderSerializer(serializers.ModelSerializer):
    discounted_price = serializers.CharField(source='discounted_price_int')
    image1 = serializers.SerializerMethodField()
    image2 = serializers.SerializerMethodField()

    def get_image1(self, obj):
        image_url = '{}{}'.format(DOMAIN, obj.image1.url) if obj.image1 else None
        return image_url

    def get_image2(self, obj):
        image_url2 = '{}{}'.format(DOMAIN, obj.image2.url) if obj.image2 else None
        return image_url2

    class Meta:
        model = Product
        fields = ['id','name','image1','image2','price','discounted','discounted_price','discount','is_new','net_sale','available']
#---------------------------
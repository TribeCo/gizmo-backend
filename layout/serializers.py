from rest_framework import serializers
from .models import Banner,FAQGroup,FAQ,Picture
from config.settings import DOMAIN
#---------------------------
class BannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        image_url2 = '{}{}'.format(DOMAIN, obj.image.url) if obj.image else None
        return image_url2
        
    class Meta:
        model = Banner
        fields = '__all__'
#---------------------------
class FAQGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQGroup
        fields = ['id', 'title']
#---------------------------
class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'name','image']
#---------------------------
class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'group', 'question', 'answer']
#---------------------------
from rest_framework import serializers
from .models import Banner,FAQGroup,FAQ
#---------------------------
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'
#---------------------------
class FAQGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQGroup
        fields = ['id', 'title']
#---------------------------
class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'group', 'question', 'answer']
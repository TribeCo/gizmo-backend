from rest_framework import serializers
from .models import *
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
    icon = serializers.SerializerMethodField()
    def get_icon(self, obj):
        icon_url = '{}{}'.format(DOMAIN, obj.icon.url) if obj.icon else None
        return icon_url
    class Meta:
        model = FAQGroup
        fields = ['id', 'title','icon']
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
class FAQSerializerForFAQG(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']
#---------------------------
class FAQGroupPageSerializer(serializers.ModelSerializer):
    faqs = FAQSerializerForFAQG(many=True)
    class Meta:
        model = FAQGroup
        fields = ['id', 'title', 'faqs']
#---------------------------
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['name', 'email', 'phoneNumber', 'title', 'text']
#---------------------------
class ConfigForAboutUsSerializer(serializers.ModelSerializer):
    gif = serializers.SerializerMethodField()

    def get_gif(self, obj):
        gif = '{}{}'.format(DOMAIN, obj.gif.url) if obj.gif else None
        return gif

    class Meta:
        model = Config
        fields = ['description', 'gif', 'address', 'phone', 'insta', 'telegram', 'email']
#---------------------------
class ConfigForEnamadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ['e_namad', 'phone', 'insta', 'telegram', 'email']
#---------------------------
class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ['title', 'text',]
    
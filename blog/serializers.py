from rest_framework import serializers
from .models import Category, Article
from accounts.models import User
from config.settings import DOMAIN
#---------------------------
class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
#---------products------------------conten
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
#---------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
#---------------------------
class UserSerializerForGizmoLog(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phoneNumber', 'full_name','id')
#---------------------------
class GizmoLogSerializer(serializers.ModelSerializer):
    Author = UserSerializerForGizmoLog()
    date = serializers.CharField(source='days_since_publish')
    cover = serializers.SerializerMethodField()

    def get_cover(self, obj):
        image_url = '{}{}'.format(DOMAIN, obj.cover.url) if obj.cover else None
        return image_url
   
    class Meta:
        model = Article
        fields = ['id','title','Author','date','cover']
#---------------------------
from itertools import product
from rest_framework import serializers
from .models import Category, Article,ArticleComment
from accounts.models import User
from config.settings import DOMAIN
from products.serializers import ProductSliderSerializer 
#---------------------------
class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
#---------------------------
class UserSerializerForGizmoLog(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phoneNumber', 'full_name','id']
#---------------------------
class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = ['id','user','text','days_since_creation']
#---------------------------
class ArticleSerializer(serializers.ModelSerializer):
    Author = UserSerializerForGizmoLog()
    comments = BlogCommentSerializer(many=True)
    products = ProductSliderSerializer(many=True)
    date = serializers.CharField(source='shamsi_date', required=False)
    class Meta:
        model = Article
        fields = ['id','title','Author','cover','slug','status','Category','views','content',
        'products','reference_name','reference_link','read_time','date',
        'comments']
#---------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
#---------------------------
class GizmoLogSerializer(serializers.ModelSerializer):
    Author = UserSerializerForGizmoLog()
    date = serializers.CharField(source='shamsi_date')
    cover = serializers.SerializerMethodField()

    def get_cover(self, obj):
        image_url = '{}{}'.format(DOMAIN, obj.cover.url) if obj.cover else None
        return image_url
   
    class Meta:
        model = Article
        fields = ['id','title','Author','date','cover','slug']
#---------------------------
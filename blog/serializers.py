from rest_framework import serializers
from .models import Category, Article
from accounts.models import User
#---------------------------
class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
#---------------------------
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
    class Meta:
        model = Article
        fields = ['id','title','Author','date']
#---------------------------
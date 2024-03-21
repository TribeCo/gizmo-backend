from importlib.metadata import requires
from typing_extensions import Required
from rest_framework import serializers
from .models import *
from .models import Comment,ProductComment
from blog.models import ArticleComment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
#---------------------------
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phoneNumber',)
#---------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
#---------------------------
class PasswordChangeRequestSerializer(serializers.ModelSerializer):
    phoneNumber = serializers.CharField()
    class Meta:
        model = User
        fields = [ 'phoneNumber']
#---------------------------
class PasswordChangeSerializer(serializers.ModelSerializer):
    phoneNumber = serializers.CharField()
    code = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        model = User
        fields = [ 'phoneNumber', 'code','password']
#---------------------------
class OldPasswordChangeSerializer(serializers.ModelSerializer):
    phoneNumber = serializers.CharField()
    new_password = serializers.CharField()
    new_password_confirm = serializers.CharField()
    class Meta:
        model = User
        fields = [ 'phoneNumber', 'new_password','password','new_password_confirm']
#---------------------------
class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phoneNumber','first_name','last_name','birth_day','gender','email')
#---------------------------
class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phoneNumber','full_name','email')
#---------------------------
class ProductCommentCreateSerializer(serializers.ModelSerializer):
    user = UserCommentSerializer(required=False)
    class Meta:
        model = ProductComment
        fields = ('user', 'text', 'anonymous','product')
#---------------------------
class ArticleCommentCreateSerializer(serializers.ModelSerializer):
    user = UserCommentSerializer(required=False)
    class Meta:
        model = ArticleComment
        fields = ('user', 'text', 'anonymous','article')
#---------------------------
class CommentSerializer(serializers.ModelSerializer):
    user_full_name = serializers.ReadOnlyField(source='user.full_name')
    class Meta:
        model = Comment
        fields = ('id', 'user', 'user_full_name', 'text', 'created', 'valid', 'rating', 'likes', 'dislikes', 'parent_comment','anonymous','days_since_creation')
#---------------------------
class ReadCommentSerializer(serializers.ModelSerializer):
    user_full_name = serializers.ReadOnlyField(source='user.full_name')
    class Meta:
        model = Comment
        fields = ( 'user', 'user_full_name', 'text', 'valid','anonymous','days_since_creation')
#---------------------------
class ArticleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = '__all__'
#---------------------------
class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = '__all__'
#---------------------------
class EnhancedTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['phoneNumber'] = user.phoneNumber
        token['email'] = user.email
        token['is_admin'] = user.is_admin
        token['is_active'] = user.is_active
        # ...
        return token
#---------------------------
class AddressSerializer(serializers.ModelSerializer):
    user = UserReadSerializer(required=False)
    class Meta:
        model = Address
        fields = ['id', 'user', 'straight_address','province', 'postal_code', 'city', 'phone_number', 'current']
#---------------------------
class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['title', 'text', 'created', 'seen', 'user']
#---------------------------
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['title', 'text', 'abs_link', 'seen', 'shamsi_date']
#---------------------------
class DeliveryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryInfo
        fields = ['name_delivery', 'phone_delivery', 'description','delivery_method']
#---------------------------
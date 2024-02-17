from rest_framework import serializers
from .models import User,Address
from .models import Comment,ArticleComment,ProductComment
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
class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phoneNumber','full_name','is_admin','is_active','email')
#---------------------------
class CommentSerializer(serializers.ModelSerializer):
    user_full_name = serializers.ReadOnlyField(source='user.full_name')
    class Meta:
        model = Comment
        fields = ('id', 'user', 'user_full_name', 'text', 'created', 'valid', 'rating', 'likes', 'dislikes', 'parent_comment')
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
    class Meta:
        model = Address
        fields = ['id', 'user', 'text', 'postal_code', 'city', 'phone_number', 'current']
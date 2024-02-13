from django.urls import path
from .views import (UserCreateAPIView,UserRetrieveAPIView,UserListAPIView,UserDeleteAPIView,UserUpdateAPIView,CreateCommentForArticleAPIView,
        CreateCommentForProductAPIView,SignUpAPIView,ReadCommentForProductAPIView,ReadCommentForArticleAPIView,DeleteCommentAPIView,UpdateCommentAPIView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
#---------------------------
urlpatterns = [
    path('users/', UserCreateAPIView.as_view(), name='user_create'),
    path('users/<int:user_id>/', UserRetrieveAPIView.as_view(), name='user_retrieve'),
    path('users/all/', UserListAPIView.as_view(), name='user_list'),
    path('users/delete/<int:user_id>/', UserDeleteAPIView.as_view(), name='user_delete'),
    path('users/update/<int:user_id>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('articles/comments/', CreateCommentForArticleAPIView.as_view(), name='create_comment_for_article'),
    path('products/comments/', CreateCommentForProductAPIView.as_view(), name='create_comment_for_product'),
    path('products/comments/<int:comment_id>/', ReadCommentForProductAPIView.as_view(), name='read_comment_for_product'),
    path('articles/comments/<int:comment_id>/', ReadCommentForArticleAPIView.as_view(), name='read_comment_for_article'),
    path('comments/delete/<int:comment_id>/', DeleteCommentAPIView.as_view(), name='delete_comment'),
    path('comments/update/<int:comment_id>/', UpdateCommentAPIView.as_view(), name='update_comment'),

    path('users/sign_up/', SignUpAPIView.as_view(), name='sign_up'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]




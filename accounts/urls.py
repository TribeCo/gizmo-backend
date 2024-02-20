from django.urls import path
from .views import *
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
    path('addresses/create/', CreateAddressAPIView.as_view(), name='create_address'),
    path('addresses/read/', ReadAddressAPIView.as_view(), name='read_addresses'),
    path('addresses/update/<int:pk>/', UpdateAddressAPIView.as_view(), name='update_address'),
    path('addresses/delete/<int:pk>/', DeleteAddressAPIView.as_view(), name='delete_address'),
    path('favorites/', FavoriteProductsAPIView.as_view(), name='favorite_products'),
    path('favorites/add/<int:pk>', AddFavoriteProductAPIView.as_view(), name='favorite_product_addtion'),
    path('favorites/delete/<int:pk>', DeleteFvaoriteProductAPIView.as_view(), name='favorite_product_deletion'),

    path('users/sign_up/', UpdateSignUpAPIView.as_view(), name='sign_up'),
    path('users/create/phone/', CreateUserWithPhoneNumberAPIView.as_view(), name='create_phone'),
    path('users/auth/code/', CheckCodeAPIView.as_view(), name='check_code'),
    path('users/check/<slug:phone_number>/', CheckPhoneNumberAPIView.as_view(), name='check_phone_number'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('orders/count/', UserOrdersCountAPIView.as_view(), name='user_orders_count'),
]




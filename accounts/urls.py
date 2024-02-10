from django.urls import path
from .views import UserCreateAPIView,UserRetrieveAPIView,UserListAPIView,UserDeleteAPIView,UserUpdateAPIView
#---------------------------
urlpatterns = [
    path('users/', UserCreateAPIView.as_view(), name='user_create'),
    path('users/<int:user_id>/', UserRetrieveAPIView.as_view(), name='user_retrieve'),
    path('users/all/', UserListAPIView.as_view(), name='user_list'),
    path('users/delete/<int:user_id>/', UserDeleteAPIView.as_view(), name='user_delete'),
    path('users/update/<int:user_id>/', UserUpdateAPIView.as_view(), name='user_update'),
]




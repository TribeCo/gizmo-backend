from django.urls import path
from .views import * 

urlpatterns = [
    path('cart/', CartDetailAPIView.as_view(),name="cart"),
    path('cart/add/', AddProductToCartAPIView.as_view(),name="cart-add"),
    path('cart/delete/<int:pk>/', DeleteProductToCartAPIView.as_view(),name="cart-delete"),
]

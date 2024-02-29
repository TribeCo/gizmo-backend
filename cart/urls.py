from django.urls import path
from .views import * 

app_name = 'cart'

urlpatterns = [
    path('cart/', CartDetailAPIView.as_view(),name="cart_detail"),
    path('cart/add/', AddProductToCartAPIView.as_view(),name="cart_add"),
    path('cart/delete/<int:pk>/', DeleteProductToCartAPIView.as_view(),name="cart_delete"),
    path('cart/item/update/<int:pk>/', CartItemUpdateView.as_view(),name="cart_item_update"),
    path('cart/clear/', ClearCartAPIView.as_view(),name="cart_clear"),
    path('coupon/', CouponCreateAPIView.as_view(),name="coupon_create"),
    path('coupon/<int:pk>/', CouponAllListAPIView.as_view(),name="coupon_read"),
    path('coupon/all/', CouponDetailView.as_view(),name="coupon_read_all"),
    path('coupon/delete/<int:pk>/', CouponDeleteView.as_view(),name="coupon_delete"),
    path('coupon/update/<int:pk>/', CouponUpdateView.as_view(),name="coupon_update"),
    path('coupon/apply/<int:pk>/', ApplyCouponToCartAPIView.as_view(),name="coupon_apply"),
]

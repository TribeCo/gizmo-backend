from django.urls import path
from .views import * 

urlpatterns = [
    path('brand/', BrandCreateAPIView.as_view(),name="brand_create"),
    path('brand/<int:pk>/', BrandDetailView.as_view(),name="brand_read"),
    path('brand/all/', BrandAllListAPIView.as_view(),name="brand_read_all"),
    path('brand/update/<int:pk>/', BrandUpdateView.as_view(),name="brand_update"),
    path('brand/delete/<int:pk>/', BrandDeleteView.as_view(),name="brand_delete"),
    path('product/', ProductCreatAPIView.as_view(),name="product_create"),
    path('product/<int:pk>/', ProductDetailView.as_view(),name="product_read"),
    path('product/<str:slug>/', ProductDetailViewBySlug.as_view(),name="product_read_slug"),
    path('product/all/', ProductListView.as_view(),name="product_read_all"),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(),name="product_update"),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(),name="product_delete"),
]

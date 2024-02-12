from django.urls import path
from .views import * 

urlpatterns = [
    path('brand/', BrandCreateAPIView.as_view(),name="brand_create"),
    path('brand/<int:pk>/', BrandDetailView.as_view(),name="brand_read"),
    path('brand/all/', BrandAllListAPIView.as_view(),name="brand_read_all"),
    path('brand/update/<int:pk>/', BrandUpdateView.as_view(),name="brand_update"),
    path('brand/delete/<int:pk>/', BrandDeleteView.as_view(),name="brand_delete"),
    path('product/', ProductCreateAPIView.as_view(),name="product_create"),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(),name="product_read"),
    path('product/<str:slug>/', ProductDetailAPIViewBySlug.as_view(),name="product_read_slug"),
    path('product/all/', ProductListAPIView.as_view(),name="product_read_all"),
    path('product/update/<int:pk>/', ProductUpdateAPIView.as_view(),name="product_update"),
    path('product/delete/<int:pk>/', ProductDeleteAPIView.as_view(),name="product_delete"),
    path('category/', CategoryCreateAPIView.as_view(),name="category_create"),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view(),name="category_read"),
    path('category/all/', CategoryListAPIView.as_view(),name="category_list"),    
    path('<str:category_name>/products/', CategoryProductsListAPIView.as_view(),name="category_articles_list"),
    path('category/update/<int:pk>/', CategoryUpdateAPIView.as_view(),name="category_update"),
    path('category/delete/<int:pk>/', CategoryDeleteAPIView.as_view(),name="category_delete"),
]

from django.urls import path
from .views import * 

urlpatterns = [
    path('brand/', BrandCreateAPIView.as_view(),name="brand_create"),
    path('brand/<int:pk>/', BrandDetailView.as_view(),name="brand_read"),
    path('brand/all/', BrandAllListAPIView.as_view(),name="brand_read_all"),
    path('brand/update/<int:pk>/', BrandUpdateView.as_view(),name="brand_update"),
    path('brand/delete/<int:pk>/', BrandDeleteView.as_view(),name="brand_delete"),
]

from django.urls import path
from .views import * 

urlpatterns = [
    path('brand/', BrandCreateAPIView.as_view(),name="brand_create"),
    path('brand/<int:id>/', FoodDetailView.as_view(),name="brand_read"),
    path('brand/<int:id>/', FoodUpdateView.as_view(),name="brand_update"),
    path('brand/<int:id>/', FoodDeleteView.as_view(),name="brand_delete"),
]

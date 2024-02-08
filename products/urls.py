from django.urls import path
from .views import * 

urlpatterns = [
    path('brand/', BrandCreateAPIView.as_view(),name="brand_create"),
]

from django.urls import path
from .views import * 

urlpatterns = [
    path('cart/', CartDetailAPIView.as_view(),name="cart"),
    
]

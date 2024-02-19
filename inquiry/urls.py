from django.urls import path
from .views import * 

urlpatterns = [
    path('foreign/order/create/', CreateForeignOrder.as_view(),name="foreign_order_create"),
]

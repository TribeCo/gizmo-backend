from django.urls import path
from .views import * 

app_name = 'inquiry'

urlpatterns = [
    path('foreign/order/create/', CreateForeignOrder.as_view(),name="foreign_order_create"),
    path('foreign/order/<int:pk>/', ForeignOrderDetailView.as_view(),name="foreign_order_read"),
    path('foreign/order/all/', ForeignOrderAllListAPIView.as_view(),name="foreign_order_read_all"),
    path('foreign/order/update/<int:pk>/', ForeignOrderUpdateView.as_view(),name="foreign_order_update"),
    path('foreign/order/delete/<int:pk>/', ForeignOrderDeleteView.as_view(),name="foreign_order_delete"),
]

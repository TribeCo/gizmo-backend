from django.urls import path
from .views import * 

app_name = 'inquiry'

urlpatterns = [
    path('foreign/order/create/', CreateForeignOrder.as_view(),name="foreign_order_create"),
    path('foreign/order/<int:pk>/', ForeignOrderDetailView.as_view(),name="foreign_order_read"),
    path('foreign/order/all/', ForeignOrderAllListAPIView.as_view(),name="foreign_order_read_all"),
    path('foreign/order/update/<int:pk>/', ForeignOrderUpdateView.as_view(),name="foreign_order_update"),
    path('foreign/order/delete/<int:pk>/', ForeignOrderDeleteView.as_view(),name="foreign_order_delete"),

    path('other/sites/', DubaiSitesCreateAPIView.as_view(),name="other_sites_create"),
    path('other/sites/<int:pk>/', DubaiSitesDetailView.as_view(),name="other_sites_read"),
    path('other/sites/all/', DubaiSitesAllListAPIView.as_view(),name="other_sites_read_all"),
    path('other/sites/update/<int:pk>/', DubaiSitesUpdateView.as_view(),name="other_sites_update"),
    path('other/sites/delete/<int:pk>/', DubaiSitesDeleteView.as_view(),name="other_sites_delete"),

    path('foreign/product/create/', ForeignProductCreateAPIView.as_view(),name="foreign_product_create"),

    
]

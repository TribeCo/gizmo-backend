from django.urls import path
from .views import * 

urlpatterns = [
    path('orders/create/', CreateOrderAPIView.as_view(),name="create_order"),
    path('orders/<int:pk>/', ReadOrderAPIView.as_view(),name="read_order"),
    path('orders/', ListOrdersAPIView.as_view(),name="list_all_orders"),
    path('orders/delete/<int:pk>/', DeleteOrderAPIView.as_view(),name="delete_order"),
    path('orders/item/set/', SetOrderItemsQuantityAPIView.as_view(),name="set_order_items_quantity"),
    path('orders/items/list/<int:pk>/', ListOrderItemsAPIview.as_view(), name="order_items_list"),
    path('orders/item/delete/<int:pk>/', DeleteProductToOrderAPIView.as_view(), name="order_items_delete"),
    path('orders/user/', ListUserOrdersAPIView.as_view(),name="user_orders"),
]

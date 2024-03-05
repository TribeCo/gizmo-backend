from django.test import SimpleTestCase
from django.urls import resolve, reverse
from orders.views import *

class OrdersUrls(SimpleTestCase):
    def test_create_order(self):
        url = reverse("orders:create_order")
        self.assertEqual(resolve(url).func.view_class, CreateOrderAPIView)

    def test_read_order(self):
        url = reverse("orders:read_order",args=[1,])
        self.assertEqual(resolve(url).func.view_class, ReadOrderAPIView)
    
    def test_list_all_orders(self):
        url = reverse("orders:list_all_orders")
        self.assertEqual(resolve(url).func.view_class, ListOrdersAPIView)
    
    def test_delete_order(self):
        url = reverse("orders:delete_order",args=[1,])
        self.assertEqual(resolve(url).func.view_class, DeleteOrderAPIView)
    
    def test_set_order_items_quantity(self):
        url = reverse("orders:set_order_items_quantity")
        self.assertEqual(resolve(url).func.view_class, SetOrderItemsQuantityAPIView)
    
    def test_order_items_list(self):
        url = reverse("orders:order_items_list", args=[1,])
        self.assertEqual(resolve(url).func.view_class, ListOrderItemsAPIview)

    def test_order_items_delete(self):
        url = reverse("orders:order_items_delete", args=[1,])
        self.assertEqual(resolve(url).func.view_class, DeleteProductToOrderAPIView)
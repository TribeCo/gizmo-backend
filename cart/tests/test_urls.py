from django.test import SimpleTestCase
from django.urls import reverse,resolve
from ..views import *
#---------------------------
class TestCartUrls(SimpleTestCase):
    def test_cart_detail(self):
        url = reverse('cart:cart_detail')
        self.assertEqual(resolve(url).func.view_class,CartDetailAPIView)

    def test_cart_add(self):
        url = reverse('cart:cart_add')
        self.assertEqual(resolve(url).func.view_class,AddProductToCartAPIView)

    def test_cart_delete(self):
        url = reverse('cart:cart_delete',args=[1,])
        self.assertEqual(resolve(url).func.view_class,DeleteProductToCartAPIView)


    def test_cart_item_update(self):
        url = reverse('cart:cart_item_update',args=[1,])
        self.assertEqual(resolve(url).func.view_class,CartItemUpdateView)

    def test_cart_clear(self):
        url = reverse('cart:cart_clear')
        self.assertEqual(resolve(url).func.view_class,ClearCartAPIView)
#---------------------------

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
class TestCouponUrls(SimpleTestCase):
    def test_coupon_create(self):
        url = reverse('cart:coupon_create')
        self.assertEqual(resolve(url).func.view_class,CouponCreateAPIView)

    def test_coupon_read(self):
        url = reverse('cart:coupon_read',args=[1,])
        self.assertEqual(resolve(url).func.view_class,CouponDetailView)

    def test_coupon_read_all(self):
        url = reverse('cart:coupon_read_all')
        self.assertEqual(resolve(url).func.view_class,CouponAllListAPIView)

    def test_coupon_delete(self):
        url = reverse('cart:coupon_delete',args=[1,])
        self.assertEqual(resolve(url).func.view_class,CouponDeleteView)

    def test_coupon_update(self):
        url = reverse('cart:coupon_update',args=[1,])
        self.assertEqual(resolve(url).func.view_class,CouponUpdateView)

    def test_coupon_apply(self):
        url = reverse('cart:coupon_apply',args=[1,])
        self.assertEqual(resolve(url).func.view_class,ApplyCouponToCartAPIView)
#---------------------------
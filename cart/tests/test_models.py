from django.test import TestCase
from ..models import *
from django.utils import timezone
from datetime import timedelta
#---------------------------
class TestCouponModel(TestCase):
    def test_model_str(self):
        coupon = Coupon.objects.create(code='Iust', valid_from=timezone.now().date(), 
                        valid_to=timezone.now().date()+ timedelta(days=1), discount=25)
        self.assertEqual(str(coupon),'25-Iust')
#---------------------------
class TestCartModel(TestCase):
    def test_model_str(self):
        user = User(
                phoneNumber = '09404016386',
                email = f"09404016386@gmail.com",
            )
        user.id = 200
        user.save()
        cart = Cart.objects.create(user=user, )
        self.assertEqual(str(cart),f'{user} - {cart.id}')
#---------------------------
class TestCartItemModel(TestCase):
    def test_model_str(self):
        user = User(
                phoneNumber = '09404016386',
                email = f"09404016386@gmail.com",
            )
        user.id = 200
        user.save()
        cart = Cart.objects.create(user=user, )

        cart_item = CartItem(cart=cart)

        self.assertEqual(str(cart),f'{user} - {cart.id}')

#---------------------------

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
from django.urls import reverse,resolve
from django.test import TestCase,Client
#---------------------------
class TestCouponAPI(TestCase):

    def setUp(self):
        self.client = Client()

    def test_create_coupon_api_200(self):
        response = self.client.post(reverse('cart:coupon_create'),data={'code':'iust','valid_from':'2024-02-04',
        'valid_to':'2024-02-06','discount':20})
        self.assertEqual(response.status_code, 201)

#---------------------------
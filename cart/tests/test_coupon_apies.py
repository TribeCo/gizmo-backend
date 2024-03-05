from django.urls import reverse,resolve
from django.test import TestCase,Client
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Coupon
from ..serializers import CouponSerializer
from django.utils import timezone
from datetime import timedelta
from ..models import *
from ..api.coupon_api import messages_for_front as messages_coupon
#---------------------------
class TestCouponAPI(TestCase):

    def setUp(self):
        self.client = Client()

    def test_create_coupon_api_200(self):
        response = self.client.post(reverse('cart:coupon_create'),data={'code':'iust','valid_from':'2024-02-04',
        'valid_to':'2024-02-06','discount':20})
        self.assertEqual(response.status_code, 201)

#---------------------------
class TestCouponAllListAPIView(APITestCase):

    def test_get_request(self):
        url = reverse('cart:coupon_read_all')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_response_data(self):
        coupon = Coupon.objects.create(code='TESTCODE',valid_from=timezone.now().date(), 
                        valid_to=timezone.now().date()+ timedelta(days=1), discount=20)
        url = reverse('cart:coupon_read_all')
        response = self.client.get(url)
        expected_data = CouponSerializer(instance=coupon).data
        self.assertEqual(response.data, [expected_data])
#---------------------------
class TestCouponDetailView(APITestCase):

    def test_get_request(self):
        coupon = Coupon.objects.create(code='TESTCODE', valid_from=timezone.now().date(), valid_to=timezone.now().date() + timedelta(days=1), discount=20)
        url = reverse('cart:coupon_read', args=[coupon.pk]) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
#---------------------------
class TestCouponDeleteView(APITestCase):

    def test_delete_request(self):
        coupon = Coupon.objects.create(code='TESTCODE', valid_from=timezone.now().date(), valid_to=timezone.now().date() + timedelta(days=1), discount=20)
        url = reverse('cart:coupon_delete', args=[coupon.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#---------------------------
class TestCouponUpdateView(APITestCase):
    
    def test_patch_request(self):
        coupon = Coupon.objects.create(code='TESTCODE', valid_from=timezone.now().date(), valid_to=timezone.now().date() + timedelta(days=1), discount=20)
        url = reverse('cart:coupon_update', args=[coupon.pk])
        updated_data = {'code': 'UPDATEDCODE'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
#---------------------------
class TestApplyCouponToCartAPIView(APITestCase):
    def test_valid_coupon(self):
        user = User(
                phoneNumber = '09404016386',
                email = f"09404016386@gmail.com",
            )
        user.save()
        cart = Cart.objects.create(user=user, )
        cart.save()

        
        self.client.force_authenticate(user=user)

        coupon = Coupon.objects.create(code='TESTCODE', valid_from=timezone.now().date(),
         valid_to=timezone.now().date() + timedelta(days=1), discount=20)

        url = reverse('cart:coupon_apply', kwargs={'pk': coupon.pk})
        response = self.client.post(url, {})
        
        user.cart.refresh_from_db()
        self.assertEqual(user.cart.discount, 20)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], messages_coupon['coupon_applied'])

    def test_invalid_coupon(self):
        user = User(
                phoneNumber = '09404016386',
                email = f"09404016386@gmail.com",
            )

        user.save()
        cart = Cart.objects.create(user=user, )
        cart.save()

        self.client.force_authenticate(user=user)

        coupon = Coupon.objects.create(code='INVALIDCODE', valid_from=timezone.now().date() + timedelta(days=1),
         valid_to=timezone.now().date() + timedelta(days=2), discount=20)

        url = reverse('cart:coupon_apply', kwargs={'pk': coupon.pk})
        response = self.client.post(url, {})
        
        user.cart.refresh_from_db()
        self.assertEqual(user.cart.discount, None) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], messages_coupon['coupon_is_not_valid'])

    def test_coupon_not_found(self):
        user = User(
                phoneNumber = '09404016386',
                email = f"09404016386@gmail.com",
            ).save()
        self.client.force_authenticate(user=user)

        url = reverse('cart:coupon_apply', kwargs={'pk': 999})  # Assuming 999 is a non-existent coupon id
        response = self.client.post(url, {})
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], messages_coupon['coupon_not_found'])
#---------------------------
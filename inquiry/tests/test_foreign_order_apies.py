from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import ForeignOrder
from ..serializers import ForeignOrderSerializer
from accounts.models import User
#---------------------------
class BaseTestForeignOrder(APITestCase):
    def setUp(self):
        user = User(
                phoneNumber = '09404016386',
                email = f"09404016386@gmail.com",
            )
        user.save()

        foreign_order = ForeignOrder.objects.create(user = user,name="Test Order", link="https://example.com", price=100)
        foreign_order.save()


        self.user = user
        self.foreign_order = foreign_order
        
#---------------------------
class TestCreateForeignOrder(BaseTestForeignOrder):
    def test_post_request(self):

        url = reverse('inquiry:foreign_order_create')
        

        data = {
            "name": "Test Order",
            "link": "https://example.com",
            "price": 100,
            "discounted": False,
            "discounted_price": 75,
            "admin_checked": False,
            "profit": 10
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='multipart')


        # Add assertions to check the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ForeignOrder.objects.count(), 2)  # Check if an order was created in the database
#---------------------------
class TestForeignOrderAllListAPIView(BaseTestForeignOrder):
    def test_get_all_foreign_orders(self):

        url = reverse('inquiry:foreign_order_read_all') 

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)


        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
#---------------------------
class TestForeignOrderDetailView(BaseTestForeignOrder):
    def test_get_foreign_order_detail(self):
        

        url = reverse('inquiry:foreign_order_read', kwargs={'pk': self.foreign_order.pk})
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # check status
        self.assertEqual(response.data['name'], "Test Order")  # check name
#---------------------------
class TestForeignOrderDeleteView(BaseTestForeignOrder):

    def test_delete_foreign_order(self):
        url = reverse('inquiry:foreign_order_delete', kwargs={'pk': self.foreign_order.pk})

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  #check status
        self.assertEqual(ForeignOrder.objects.count(), 0)  # check db
#---------------------------
class TestForeignOrderUpdateView(BaseTestForeignOrder):
    def test_update_foreign_order(self):
        url = reverse('inquiry:foreign_order_update', kwargs={'pk': self.foreign_order.pk})
        data = {
            "name": "Updated Order",
            "price": 150
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')


        self.assertEqual(response.status_code, status.HTTP_200_OK)  # check status
        updated_order = ForeignOrder.objects.get(pk=self.foreign_order.pk)
        self.assertEqual(updated_order.name, "Updated Order")  # update name
        self.assertEqual(updated_order.price, 150)
#---------------------------
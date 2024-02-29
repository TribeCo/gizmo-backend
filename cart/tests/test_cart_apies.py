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
from ..api.cart_api import messages_for_front as messages_cart
from products.models import *
#---------------------------
class TestCartPIView(APITestCase):
    def setUp(self):
        category = Category.objects.create(name='Electronics',slug='Electronics')
        brand = Brand.objects.create(name='ABC',slug='ABC',logo="src",description="abcf")
        color1 = Color.objects.create(name="test_color",en="test_en",code="123")

        product = Product.objects.create(
            name='Test Product',
            brand=brand,
            price=100,
            image='path_to_image.jpg',
            alt='Test Product Image',
            short_description='Short description of the product',
            description='Detailed description of the product',
            warehouse=10,
            created=timezone.now(),
            updated=timezone.now(),
        )

        product.colors.add(color1)
        product.category.add(category)

        color1.save()
        product.save()
        category.save()
        brand.save()

        self.product = product
        self.color = color1
#---------------------------
class TestCartDetailAPIView(TestCartPIView):

    def test_get_request(self):
        user = User(
                phoneNumber = '09404016386',
                email = f"09404016386@gmail.com",
            )
        user.save()

        cart = Cart.objects.create(user=user)
        prodcut = Product()
        item1 = CartItem.objects.create(cart=cart, price=100, quantity=2,color=self.color,product=self.product)
        item2 = CartItem.objects.create(cart=cart, price=50, quantity=3,color=self.color,product=self.product) 


        url = reverse('cart:cart_detail')
        self.client.force_authenticate(user=user)
        response = self.client.get(url)

 

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cart']['id'], cart.id)
        self.assertEqual(response.data['cart']['user']['id'], user.id)
#---------------------------
class TestAddProductToCartAPIView(TestCartPIView):

    def test_post_request(self):
        user = User.objects.create(phoneNumber='09404016386', email='09404016386@gmail.com')
        user.save()

        # Create a cart for the user
        cart = Cart.objects.create(user=user)

        url = reverse('cart:cart_add')
        data = {
            "quantity": 1,
            "color": 1,  # Color id
            "product": 1  # Product id
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')

        # Add assertions to check the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Add more assertions as needed to check the response data

        # Clean up after the test if needed
#---------------------------
class TestDeleteProductToCartAPIView(TestCartPIView):
    
    def test_delete_request(self):
        # Create a user and a cart for the user
        user = User.objects.create(phoneNumber='09404016386', email='09404016386@gmail.com')
        user.save()
        cart = Cart.objects.create(user=user)

        # Create a CartItem to delete
        item = CartItem.objects.create(cart=cart, price=100, quantity=2, color=self.color, product=self.product)

        url = reverse('cart:cart_delete', kwargs={'pk': item.id})
        self.client.force_authenticate(user=user)
        response = self.client.delete(url)

        # Add assertions to check the response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Add more assertions as needed to check the response data

        # Clean up after the test if needed
#---------------------------
class TestCartItemUpdateView(TestCartPIView):
    def test_put_request(self):
        # Create a user and a cart for the user
        user = User.objects.create(phoneNumber='09404016386', email='09404016386@gmail.com')
        user.save()
        cart = Cart.objects.create(user=user)

        # Create a CartItem to update
        item = CartItem.objects.create(cart=cart, price=100, quantity=2, color=self.color, product=self.product)

        url = reverse('cart:cart_item_update', kwargs={'pk': item.id})
        data = {
            "quantity": 3,
            "color": self.color.id,  # New color id
            "product": self.product.id  # New product id
        }
        self.client.force_authenticate(user=user)
        response = self.client.put(url, data, format='json')

        # Add assertions to check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions as needed to check the response data

        # Clean up after the test if needed
#---------------------------
class TestClearCartAPIView(TestCartPIView):
    def test_post_request(self):
        # Create a user and a cart for the user
        user = User.objects.create(phoneNumber='09404016386', email='09404016386@gmail.com')
        user.save()
        cart = Cart.objects.create(user=user)

        # Create some CartItems in the cart
        item1 = CartItem.objects.create(cart=cart, price=100, quantity=2,  color=self.color, product=self.product)
        item2 = CartItem.objects.create(cart=cart, price=50, quantity=3,  color=self.color, product=self.product)

        url = reverse('cart:cart_clear')
        self.client.force_authenticate(user=user)
        response = self.client.post(url)

        # Add assertions to check the response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Add more assertions as needed to check the response data

        # Clean up after the test if needed
#---------------------------
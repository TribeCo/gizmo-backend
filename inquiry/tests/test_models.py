from django.test import TestCase
from ..models import *
#---------------------------
class TestForeignOrderModel(TestCase):
    def test_model_str(self):
        user = User(
                phoneNumber = '09404016386',
                email = f"09404016386@gmail.com",
            )
        user.save()
        order = ForeignOrder.objects.create(
            user=user,
            name='Test Order',
            link='https://example.com',
            price=100,
            discounted=False,
            discounted_price=75,
            image='path_to_image.jpg',
            admin_checked=False,
            profit=10
        )
        self.assertEqual(str(order), 'Test Order - 100')
#---------------------------

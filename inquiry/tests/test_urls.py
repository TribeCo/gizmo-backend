from django.test import SimpleTestCase
from django.urls import reverse,resolve
from ..views import *
#---------------------------
class TestInquiryUrls(SimpleTestCase):
    def test_foreign_order_create(self):
        url = reverse('inquiry:foreign_order_create')
        self.assertEqual(resolve(url).func.view_class,CreateForeignOrder)

    def test_foreign_order_read(self):
        url = reverse('inquiry:foreign_order_read',args=[1,])
        self.assertEqual(resolve(url).func.view_class,ForeignOrderDetailView)

    def test_foreign_order_read_all(self):
        url = reverse('inquiry:foreign_order_read_all')
        self.assertEqual(resolve(url).func.view_class,ForeignOrderAllListAPIView)


    def test_foreign_order_update(self):
        url = reverse('inquiry:foreign_order_update',args=[1,])
        self.assertEqual(resolve(url).func.view_class,ForeignOrderUpdateView)

    def test_foreign_order_delete(self):
        url = reverse('inquiry:foreign_order_delete',args=[1,])
        self.assertEqual(resolve(url).func.view_class,ForeignOrderDeleteView)
#---------------------------
from django.test import SimpleTestCase
from django.urls import reverse,resolve
from ..views import *
#---------------------------
class TestBannerUrls(SimpleTestCase):
    def test_create_banner_url(self):
        url = reverse('layout:create_banner')
        self.assertEqual(resolve(url).func.view_class, CreateBannerAPIView)

    def test_delete_banner_url(self):
        url = reverse('layout:delete_banner', args=[1,]) 
        self.assertEqual(resolve(url).func.view_class, DeleteBannerAPIView)

    def test_update_banner_url(self):
        url = reverse('layout:update_banner', args=[1,]) 
        self.assertEqual(resolve(url).func.view_class, UpdateBannerAPIView)

    def test_read_banner_url(self):
        url = reverse('layout:read_banner', kwargs={'slug': 'example-slug'})
        self.assertEqual(resolve(url).func.view_class, ReadBannerBySlugAPIView)
#---------------------------
class TestLayoutUrls(SimpleTestCase):
    def test_picture_create_url(self):
        url = reverse('layout:picture_create')
        self.assertEqual(resolve(url).func.view_class, PictureCreateAPIView)

    def test_picture_read_url(self):
        url = reverse('layout:picture_read', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, PictureDetailView)

    def test_picture_read_all_url(self):
        url = reverse('layout:picture_read_all')
        self.assertEqual(resolve(url).func.view_class, PictureAllListAPIView)

    def test_picture_update_url(self):
        url = reverse('layout:picture_update', kwargs={'pk': 1}) 
        self.assertEqual(resolve(url).func.view_class, PictureUpdateView)

    def test_picture_delete_url(self):
        url = reverse('layout:picture_delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, PictureDeleteView)
#---------------------------
class TestFAQGroupUrls(SimpleTestCase):
    def test_create_faq_group_url(self):
        url = reverse('layout:create_faq_group')
        self.assertEqual(resolve(url).func.view_class, CreateFAQGroupAPIView)

    def test_read_faq_groups_url(self):
        url = reverse('layout:read_faq_groups')
        self.assertEqual(resolve(url).func.view_class, ReadFAQGroupAPIView)

    def test_update_faq_group_url(self):
        url = reverse('layout:update_faq_group', kwargs={'pk': 1}) 
        self.assertEqual(resolve(url).func.view_class, UpdateFAQGroupAPIView)

    def test_delete_faq_group_url(self):
        url = reverse('layout:delete_faq_group', kwargs={'pk': 1}) 
        self.assertEqual(resolve(url).func.view_class, DeleteFAQGroupAPIView)
#---------------------------
class TestFAQUrls(SimpleTestCase):
    def test_create_faq_url(self):
        url = reverse('layout:create_faq')
        self.assertEqual(resolve(url).func.view_class, CreateFAQAPIView)

    def test_read_faqs_url(self):
        url = reverse('layout:read_faqs')
        self.assertEqual(resolve(url).func.view_class, ReadFAQAPIView)

    def test_update_faq_url(self):
        url = reverse('layout:update_faq', kwargs={'pk': 1}) 
        self.assertEqual(resolve(url).func.view_class, UpdateFAQAPIView)

    def test_delete_faq_url(self):
        url = reverse('layout:delete_faq', kwargs={'pk': 1}) 
        self.assertEqual(resolve(url).func.view_class, DeleteFAQAPIView)

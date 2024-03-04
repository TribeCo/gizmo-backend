from django.test import TestCase
from ..models import *
from django.utils import timezone
from datetime import timedelta
#--------------------------
class TestFAQGroupModel(TestCase):
    def test_string_representation(self):
        faq_group = FAQGroup.objects.create(title='Test FAQ Group')
        self.assertEqual(str(faq_group), 'Test FAQ Group')
#--------------------------
class TestFAQModel(TestCase):
    def test_string_representation(self):
        faq_group = FAQGroup.objects.create(title='Test FAQ Group')
        faq = FAQ.objects.create(group=faq_group, question='Test Question', answer='Test Answer')
        self.assertEqual(str(faq), 'Test Question')
#--------------------------
class TestPictureModel(TestCase):
    def test_string_representation(self):
        picture = Picture.objects.create(name='Test Picture')
        self.assertEqual(str(picture), 'Test Picture')
#--------------------------
class TestBannerModel(TestCase):
    def setUp(self):
        banner = Banner.objects.create(bigTitle="Test Banner",  for_what="T",color_title="FFF", abs_link="url")
        banner.save()
        self.banner = banner

    def test_string_representation(self):
        self.assertEqual(str(self.banner), 'Test Banner')

    def test_get_absolute_url(self):
        self.assertEqual(self.banner.get_absolute_url(), 'url')


    def test_filter_method(self):
        Banner.objects.create(bigTitle='Banner 1', for_what='A',color_title="FFF", abs_link="test_main_link")
        Banner.objects.create(bigTitle='Banner 2', for_what='S',color_title="FFF", abs_link="test_main_link")
        Banner.objects.create(bigTitle='Banner 3', for_what='T',color_title="FFF", abs_link="test_main_link")

        banners = Banner.objects.filter(for_what='T').count()

        self.assertEqual(banners, 2)
#--------------------------
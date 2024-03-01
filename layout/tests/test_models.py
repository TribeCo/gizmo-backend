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
# class TestBannerModel(TestCase):
#     def test_string_representation(self):
#         banner = Banner.objects.create(bigTitle='Test Banner', smallTitle='Test Small Title', for_what='T', main_link='test', out_link='test')
#         self.assertEqual(str(banner), 'Test Banner')

#     def test_get_absolute_url(self):
#         banner = Banner.objects.create(bigTitle='Test Banner', smallTitle='Test Small Title', for_what='T', main_link='test', out_link='test')
#         self.assertEqual(banner.get_absolute_url(), '/test/test/')


#     def test_filter_method(self):
#         Banner.objects.create(bigTitle='Banner 1', smallTitle='Small Title 1', for_what='T', main_link='test', out_link='test')
#         Banner.objects.create(bigTitle='Banner 2', smallTitle='Small Title 2', for_what='S', main_link='test', out_link='test')
#         Banner.objects.create(bigTitle='Banner 3', smallTitle='Small Title 3', for_what='T', main_link='test', out_link='test')

#         banners = Banner.filter()

#         self.assertEqual(len(banners['T']), 2)
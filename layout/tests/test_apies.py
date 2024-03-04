from django.urls import resolve,reverse
from django.test import client,TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from ..views import *
#---------------------------
# class TestCreateBannerAPIView(APITestCase):
#     def test_create_banner_api_201(self):
#         data = {
#             "bigTitle": "Test Banner",
#             "smallTitle": "Small Test Banner",
#             "image": "test_image.jpg",
#             "for_what": "T",
#             "main_link": "test_main_link",
#             "out_link": "test_out_link"
#         }
#         response = self.client.post('/api/banners/create/', data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#---------------------------
class TestReadBannerBySlugAPIView(APITestCase):

    def test_read_banner_by_slug_api_200(self):
        banner = Banner.objects.create(bigTitle="Test Banner",  for_what="T",color_title="FFF", abs_link="test_main_link")
        response = self.client.get(f'/api/banners/read/{banner.for_what}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_banner_by_invalid_slug_api_404(self):
        response = self.client.get('/api/banners/read/invalid_slug/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#---------------------------
class TestDeleteBannerAPIView(APITestCase):
    def test_delete_banner_api_204(self):
        banner = Banner.objects.create(bigTitle="Test Banner", for_what="T",color_title="FFF", abs_link="test_main_link")
        response = self.client.delete(f'/api/banners/delete/{banner.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_banner_api_404(self):
        response = self.client.delete('/api/banners/delete/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#---------------------------
# class TestUpdateBannerAPIView(APITestCase):
#     def test_update_banner_api_200(self):
#         banner = Banner.objects.create(bigTitle="Test Banner", smallTitle="Small Test Banner", for_what="T", main_link="test_main_link", out_link="test_out_link")
#         data = {
#             "bigTitle": "Updated Test Banner",
#             "smallTitle": "Updated Small Test Banner",
#             "image": "test_updated_image.jpg",
#             "for_what": "T",
#             "main_link": "test_updated_main_link",
#             "out_link": "test_updated_out_link"
#         }
#         response = self.client.put(f'/api/banners/update/{banner.id}/', data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_update_invalid_banner_api_404(self):
#         data = {
#             "bigTitle": "Updated Test Banner",
#             "smallTitle": "Updated Small Test Banner",
#             "image": "test_updated_image.jpg",
#             "for_what": "T",
#             "main_link": "test_updated_main_link",
#             "out_link": "test_updated_out_link"
#         }
#         response = self.client.put('/api/banners/update/9999/', data)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#---------------------------
#---------------------------
#---------------------------
#---------------------------
#---------------------------
#---------------------------
#---------------------------
#---------------------------
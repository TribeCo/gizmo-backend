from django.test import TestCase
from ..models import *
from django.core.files.uploadedfile import SimpleUploadedFile
#---------------------------
class TestBrandModel(TestCase):
    def test_string_representation(self):
        brand = Brand.objects.create(name='Test Brand', description='Test Description')
        self.assertEqual(str(brand), 'Test Brand')
#---------------------------
class TestCategoryModel(TestCase):
    def test_string_representation(self):
        category = Category.objects.create(name='Test Category', sub_category=None, is_sub=False, is_for_landing=False)
        self.assertEqual(str(category), 'Test Category')
        
    def test_slug_generation(self):
        category = Category.objects.create(name='Test Category', sub_category=None, is_sub=False, is_for_landing=False)
        self.assertEqual(category.slug, 'Test-Category')
#---------------------------
class TestColorModel(TestCase):
    def test_string_representation(self):
        color = Color.objects.create(name='قرمز', en='red', code='FF0000')
        self.assertEqual(str(color), 'قرمز')
#---------------------------
# class TestProductModel(TestCase):
#---------------------------
class TestProductImageModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(
            name='Test Product',
            En='Test Product',
            slug='test-product',
            price=100,
            image=SimpleUploadedFile("test_image.jpg", b"file_content"),
            alt='Test Product Image',
            is_available=True,
            short_description='Short description of test product',
            description='Description of test product',
            more_info='More info about test product',
        )

    def test_string_representation(self):
        product_image = ProductImage.objects.create(
            image=SimpleUploadedFile("product_image.jpg", b"file_content"),
            is_main=False,
            product=self.product,
            alt='Product Image',
        )
        self.assertEqual(str(product_image), f"{self.product} - {product_image.id}")


from rest_framework.test import APITestCase,force_authenticate,APIClient
from rest_framework import status
from django.urls import reverse
from ..models import *
from ..serializers import *
from django.contrib.auth.hashers import make_password
from accounts.models import User
from django.test import TestCase
#---------------------------
# class TestBrandCreateAPIView(APITestCase):
#     def test_brand_create_api_201(self):
#         data = {
#             "name": "Test Brand",
#             "slug": "test-brand",
#             "logo": "test_logo.jpg",
#             "description": "Test description"
#         }
#         response = self.client.post(reverse('brand_create'), data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_invalid_brand_create_api_400(self):
#         data = {
#             "name": "",  # Invalid data
#             "slug": "test-brand",
#             "logo": "test_logo.jpg",
#             "description": "Test description"
#         }
#         response = self.client.post(reverse('brand_create'), data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#---------------------------
class TestBrandAllListAPIView(APITestCase):
    def setUp(self):
        Brand.objects.create(name='Brand1', slug='brand1', description='Description of Brand1')
        Brand.objects.create(name='Brand2', slug='brand2', description='Description of Brand2')
        Brand.objects.create(name='Brand3', slug='brand3', description='Description of Brand3')

    def test_brand_all_list_api_view(self):
        url = '/api/brand/all/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        self.assertEqual(response.data, serializer.data)
#---------------------------
class TestBrandDetailView(APITestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Test Brand', slug='test-brand', description='Description of Test Brand')

    def test_brand_detail_view(self):
        url = f'/api/brand/{self.brand.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = BrandSerializer(self.brand)
        self.assertEqual(response.data, serializer.data)
#---------------------------
# class TestBrandDeleteView(APITestCase):
#     def setUp(self):
#         self.brand = Brand.objects.create(name="Test Brand")
#         self.user = User.objects.create(username='testuser', password='12345')

#     def test_delete_brand_api_204(self):
#         self.client.force_authenticate(user=self.user)

#         response = self.client.delete(reverse('products:brand_delete', kwargs={'pk': self.brand.pk}))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#     def test_delete_invalid_brand_api_404(self):
#         self.client.force_authenticate(user=self.user)

#         response = self.client.delete(reverse('products:brand_delete', kwargs={'pk': 9999}))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#---------------------------
# class TestBrandUpdateView(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.client.login(username='testuser', password='testpassword')
#         self.brand = Brand.objects.create(name="Test Brand")

#     def test_update_brand_api_200(self):
#         data = {"name": "Updated Brand Name"}
#         url = reverse('products:brand_update', kwargs={'pk': self.brand.pk})

#         response = self.client.put(url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_update_invalid_brand_api_404(self):
#         data = {"name": "Updated Brand Name"}
#         url = reverse('products:brand_update', kwargs={'pk': 9999})

#         response = self.client.put(url, data)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#---------------------------
# class TestCategoryCreateAPIView(APITestCase):
#---------------------------
class TestCategoryDetailAPIView(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category", slug="test-category")

    def test_get_category_api_200(self):
        url = reverse('products:category_read', kwargs={'pk': self.category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_category_api_404(self):
        url = reverse('products:category_read', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#---------------------------
# class TestCategoryDeleteAPIView(APITestCase):
#---------------------------
# class TestCategoryUpdateAPIView(APITestCase):
#---------------------------
class TestCategoryListAPIView(APITestCase):
    def setUp(self):
        Category.objects.create(name="Category 1", slug="category-1")
        Category.objects.create(name="Category 2", slug="category-2")

    def test_get_categories_api_200(self):
        url = reverse('products:category_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Category.objects.count())
#---------------------------
# class TestCategoryProductsListAPIView(APITestCase):
#---------------------------
# class TestCategotyLandingListAPIView(APITestCase):
#     def setUp(self):
#         Category.objects.create(name="Test Category 1", is_for_landing=True)
#         Category.objects.create(name="Test Category 2", is_for_landing=True)
#         Category.objects.create(name="Test Category 3", is_for_landing=True)
#         Category.objects.create(name="Test Category 4", is_for_landing=True)
    
#     def test_retrieve_categories_for_landing_page(self):
#         response = self.client.get(reverse('products:category_landing'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(len(response.data['data']) <= 4)

#     def test_no_categories_for_landing_page(self):
#         Category.objects.filter(is_for_landing=True).delete()
#         response = self.client.get(reverse('products:category_landing'))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data['message'], 'No categories suitable for landing page found.')
#---------------------------
# class TestProductCreateAPIView(APITestCase):
#     def setUp(self):
#         self.valid_payload = {
#             "name": "New Product",
#             "slug": "new-product",
#             "price": 200,
#             "image": "new.jpg",
#             "alt": "New image",
#             "short_description": "Short description",
#             "description": "Description",
#             "more_info": "More info"
#         }

#         self.invalid_payload = {
#             # Invalid payload missing required fields
#         }

#     def test_create_product_api_view_valid_payload(self):
#         url = reverse('products:product_create')
#         response = self.client.post(url, data=self.valid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(Product.objects.filter(name='New Product').exists())

#     def test_create_product_api_view_invalid_payload(self):
#         url = reverse('products:product_create')
#         response = self.client.post(url, data=self.invalid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertFalse(Product.objects.filter(name='New Product').exists())
#---------------------------
class TestProductDetailAPIView(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Test Product', slug='test-product', price=100, image='test.jpg', alt='Test image', short_description='Short description', description='Description', more_info='More info')

    def test_retrieve_product_detail_api_view(self):
        url = reverse('products:product_read', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ProductSerializer(self.product)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_invalid_product_detail_api_404(self):
        url = reverse('products:product_read', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#---------------------------
class TestProductDetailAPIViewBySlug(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Test Product', slug='test-product', price=100)

    def test_retrieve_product_by_slug_api_view(self):
        url = reverse('products:product_read_slug', kwargs={'slug': self.product.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_retrieve_product_by_invalid_slug_api_view(self):
        url = reverse('products:product_read_slug', kwargs={'slug': 'invalid-slug'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#---------------------------
class TestProductListAPIView(APITestCase):
    def setUp(self):
        Product.objects.create(name='Product1', slug='product1', price=100)
        Product.objects.create(name='Product2', slug='product2', price=200)

    def test_list_all_products_api_view(self):
        url = reverse('products:product_read_all')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
#---------------------------
# class TestProductDeleteAPIView(APITestCase):
#     def setUp(self):
#         self.product = Product.objects.create(name='Test Product', slug='test-product', price=100)

#     def test_delete_product_api_view(self):
#         url = reverse('products:product_delete', kwargs={'pk': self.product.pk})
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

#     def test_delete_invalid_product_api_view(self):
#         url = reverse('products:product_delete', kwargs={'pk': 9999})
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#---------------------------
# class TestProductUpdateAPIView(APITestCase):
#     def setUp(self):
#         self.product = Product.objects.create(name='Test Product', slug='test-product', price=100)
#         self.valid_payload = {'name': 'Updated Product Name', 'price': 200}

#     def test_update_product_api_view(self):
#         url = reverse('products:product_update', kwargs={'pk': self.product.pk})
#         response = self.client.put(url, self.valid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.product.refresh_from_db()
#         self.assertEqual(self.product.name, 'Updated Product Name')
#         self.assertEqual(self.product.price, 200)

#     def test_update_invalid_product_api_view(self):
#         url = reverse('products:product_update', kwargs={'pk': 9999})
#         response = self.client.put(url, self.valid_payload, format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#---------------------------
# Error:django.db.utils.IntegrityError: UNIQUE constraint failed: products_product.slug
# class TestProductDiscountedListAPIView(APITestCase):
#     def setUp(self):
#         self.product1 = Product.objects.create(name='Product 1', price=100, discounted=True)
#         self.product2 = Product.objects.create(name='Product 2', price=200, discounted=False)
#         self.product3 = Product.objects.create(name='Product 3', price=300, discounted=True)

#     def test_retrieve_discounted_products(self):
#         url = reverse('products:all_discounted_products')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['data']), 2)
#         self.assertEqual(response.data['data'][0]['name'], 'Product 1')
#         self.assertEqual(response.data['data'][1]['name'], 'Product 3')

#     def test_no_discounted_products_available(self):
#         Product.objects.all().update(discounted=False)
#         url = reverse('products:all_discounted_products')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['data']), 0)
#---------------------------
# class TestSimilarProductsAPIView(APITestCase):
#     def setUp(self):
#         self.product = Product.objects.create(name='Test Product', price=100)
#         self.similar_product1 = Product.objects.create(name='Similar Product 1', price=150)
#         self.similar_product2 = Product.objects.create(name='Similar Product 2', price=200)

#     def test_retrieve_similar_products(self):
#         url = reverse('products:similar_products')
#         data = {'id': self.product.id}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['data']), 2)
#         self.assertEqual(response.data['data'][0]['name'], 'Similar Product 1')
#         self.assertEqual(response.data['data'][1]['name'], 'Similar Product 2')

#     def test_invalid_product_id(self):
#         url = reverse('products:similar_products')
#         data = {'id': 9999}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#---------------------------
class TestNewProductAPIView(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_new_products(self):
        url = reverse('products:product_news')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
#---------------------------
# class TestObservedProductAPIView(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.client.force_login(self.user)

#     def test_get_observed_products(self):
#         url = reverse('products:product_observed')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#---------------------------
class TestProductSearchAPIView(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_search_products(self):
        url = reverse('products:product_search', kwargs={'slug': 'test-slug'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

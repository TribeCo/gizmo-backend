from django.test import SimpleTestCase
from django.urls import reverse,resolve
from ..views import *
#---------------------------
class TestBrandUrls(SimpleTestCase):
    def test_create_brand_url(self):
        url = reverse('products:brand_create')
        self.assertEqual(resolve(url).func.view_class, BrandCreateAPIView)

    def test_detail_brand_url(self):
        url = reverse('products:brand_read', args=[1,])
        self.assertEqual(resolve(url).func.view_class, BrandDetailView)

    def test_all_brands_url(self):
        url = reverse('products:brand_read_all')
        self.assertEqual(resolve(url).func.view_class, BrandAllListAPIView)

    def test_update_brand_url(self):
        url = reverse('products:brand_update', args=[1,])
        self.assertEqual(resolve(url).func.view_class, BrandUpdateView)

    def test_delete_brand_url(self):
        url = reverse('products:brand_delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, BrandDeleteView)
#---------------------------
class TestProductUrls(SimpleTestCase):
    def test_create_product_url(self):
        url = reverse('products:product_create')
        self.assertEqual(resolve(url).func.view_class, ProductCreateAPIView)

    def test_list_products_url(self):
        url = reverse('products:product_read_all')
        self.assertEqual(resolve(url).func.view_class, ProductListAPIView)

    def test_similar_products_url(self):
        url = reverse('products:similar_products')
        self.assertEqual(resolve(url).func.view_class, SimilarProductsAPIView)

    def test_new_product_url(self):
        url = reverse('products:product_news')
        self.assertEqual(resolve(url).func.view_class, NewProductAPIView)

    def test_observed_product_url(self):
        url = reverse('products:product_observed')
        self.assertEqual(resolve(url).func.view_class, ObservedProductAPIView)

    def test_detail_product_by_id_url(self):
        url = reverse('products:product_read', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductDetailAPIView)

    def test_detail_product_by_slug_url(self):
        url = reverse('products:product_read_slug', kwargs={'slug': 'example-slug'})
        self.assertEqual(resolve(url).func.view_class, ProductDetailAPIViewBySlug)

    def test_update_product_url(self):
        url = reverse('products:product_update', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductUpdateAPIView)

    def test_delete_product_url(self):
        url = reverse('products:product_delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductDeleteAPIView)

    # def test_discounted_products_url(self):
    #     url = reverse('products:all_discounted_products')
    #     self.assertEqual(resolve(url).func.view_class, ProductDiscountedListAPIView)

    def test_product_search_url(self):
        url = reverse('products:product_search', kwargs={'slug': 'example-slug'})
        self.assertEqual(resolve(url).func.view_class, ProductSearchAPIView)
#---------------------------
class TestCategoryUrls(SimpleTestCase):
    def test_category_create_url(self):
        url = reverse('products:category_create')
        self.assertEqual(resolve(url).func.view_class, CategoryCreateAPIView)

    def test_category_landing_url(self):
        url = reverse('products:category_landing')
        self.assertEqual(resolve(url).func.view_class, CategotyLandingListAPIView)

    def test_category_read_url(self):
        url = reverse('products:category_read', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, CategoryDetailAPIView)

    def test_category_list_url(self):
        url = reverse('products:category_list')
        self.assertEqual(resolve(url).func.view_class, CategoryListAPIView)

    def test_category_articles_list_url(self):
        url = reverse('products:category_articles_list', kwargs={'category_name': 'example-category'})
        self.assertEqual(resolve(url).func.view_class, CategoryProductsListAPIView)

    def test_category_update_url(self):
        url = reverse('products:category_update', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, CategoryUpdateAPIView)

    def test_category_delete_url(self):
        url = reverse('products:category_delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, CategoryDeleteAPIView)

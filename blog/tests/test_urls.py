from django.test import SimpleTestCase
from django.urls import resolve, reverse
from ..views import *

class ArticleUrls(SimpleTestCase):
    def test_article_create(self):
        url = reverse("blog:article_create")
        self.assertEqual(resolve(url).func.view_class, ArticleCreateAPIView)

    def test_article_read(self):
        url = reverse("blog:article_read")
        self.assertEqual(resolve(url).func.view_class, ArticleDetailView)

    def test_article_list(self):
        url = reverse("blog:article_list")
        self.assertEqual(resolve(url).func.view_class, ArticleListView)

    def test_article_update(self):
        url = reverse("blog:article_update")
        self.assertEqual(resolve(url).func.view_class, ArticleUpdateView)
    
    def test_article_delete(self):
        url = reverse("blog:article_delete")
        self.assertEqual(resolve(url).func.view_class, ArticleDeleteAPIView)
        
    def test_last_three_gizmo_logs(self):
        url = reverse("blog:last-three-gizmo-logs")
        self.assertEqual(resolve(url).func.view_class, LastThreeGizmologs)

class CategoryUrls(SimpleTestCase):
    def test_category_create(self):
        url = reverse("blog:category_create")
        self.assertEqual(resolve(url).func.view_class, CategoryCreateAPIView)
    
    def test_category_read(self):
        url = reverse("blog:category_read")
        self.assertEqual(resolve(url).func.view_class, CategoryDetailAPIVeiw)
    
    def test_category_list(self):
        url = reverse("blog:category_list")
        self.assertEqual(resolve(url).func.view_class, CategoryListAPIView)
    
    def test_category_articles_list(self):
        url = reverse("blog:category_articles_list")
        self.assertEqual(resolve(url).func.view_class, CategoryArticlesAPIView)
    
    def test_category_update(self):
        url = reverse("blog:category_update")
        self.assertEqual(resolve(url).func.view_class, CategoryUpdateAPIVeiw)
    
    def test_category_delete(self):
        url = reverse("blog:category_delete")
        self.assertEqual(resolve(url).func.view_class, CategoryDeleteAPIVew)

    

    
    


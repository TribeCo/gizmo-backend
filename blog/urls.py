from django.urls import path
from .views import * 

urlpatterns = [
    path('article/', ArticleCreateAPIView.as_view(),name="article_create"),
    path('article/<int:pk>/', ArticleDetailView.as_view(),name="article_read"),
    path('article/all/', ArticleListView.as_view(),name="article_list"),
    path('article/update/<int:pk>/', ArticleUpdateView.as_view(),name="article_update"),
    path('article/delete/<int:pk>/', ArticleDeleteAPIView.as_view(),name="article_delete"),
    path('article/similar/<int:pk>/', SimilarArticle.as_view(),name="similar_article"),
    path('article/<slug:slug>/', ArticleDetailSlugView.as_view(),name="article_read_with_slug"),

    path('landing/', LastThreeGizmologs.as_view(),name="last_three_gizmologs"),
    path('news/', NewsGizmologs.as_view(),name="news_gizmologs"),
    path('popular/', PopularGizmologs.as_view(),name="popular_gizmologs"),

    path('category/', CategoryCreateAPIView.as_view(),name="category_create"),
    path('category/<int:pk>/', CategoryDetailAPIVeiw.as_view(),name="category_read"),
    path('category/all/', CategoryListAPIView.as_view(),name="category_list"),    
    path('<str:category_title>/articles/', CategoryArticlesAPIView.as_view(),name="category_articles_list"),
    path('category/update/<int:pk>/', CategoryUpdateAPIVeiw.as_view(),name="category_update"),
    path('category/delete/<int:pk>/', CategoryDeleteAPIVew.as_view(),name="category_delete"),
]

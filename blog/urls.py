from django.urls import path
from .views import * 

urlpatterns = [
    path('article/', ArticleCreateAPIView.as_view(),name="article_create"),
    path('article/<int:pk>/', ArticleDetailView.as_view(),name="article_read"),    
    path('article/all/', ArticleListView.as_view(),name="article_list"),
    path('article/update/<int:pk>/', ArticleUpdateView.as_view(),name="article_update"),
    path('article/delete/<int:pk>/', ArticleDeleteAPIView.as_view(),name="article_delete"),
    path('category/', CategoryCreateAPIView.as_view(),name="Category_create"),
    path('category/<int:pk>/', CategoryDetailAPIVeiw.as_view(),name="Category_read"),    
    path('category/all/', CategoryListAPIView.as_view(),name="Category_list"),
    path('category/update/<int:pk>/', CategoryUpdateAPIVeiw.as_view(),name="Category_update"),
    path('category/delete/<int:pk>/', CategoryDeleteAPIVew.as_view(),name="Category_delete"),
]

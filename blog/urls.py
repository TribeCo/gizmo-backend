from django.urls import path
from .views import * 

urlpatterns = [
    path('article/', ArticleCreateAPIView.as_view(),name="article_create"),
    path('article/<int:pk>/', ArticleDetailView.as_view(),name="article_read"),    
    path('article/all/', ArticleListView.as_view(),name="article_list"),
    path('article/update/<int:pk>/', ArticleUpdateView.as_view(),name="article_update"),
    path('article/delete/<int:pk>/', ArticleDeleteAPIView.as_view(),name="article_delete"),
]

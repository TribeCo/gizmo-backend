from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from .serializers import *
from .models import Article, Category


#Article API views

class ArticleCreateAPIView(APIView):    
    """Creating an Article"""
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'مقاله ساخته شد', 'data': serializer.data})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ArticleDetailView(generics.RetrieveAPIView):
    """Getting the details of an Article with ID(domain.com/..../pk/)"""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer    
#---------------------------
class ArticleUpdateView(generics.UpdateAPIView):
    """Updating the informations of an Article with ID(domain.com/..../pk/)"""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer    
#---------------------------
class ArticleDeleteAPIView(generics.DestroyAPIView):
    """Deleting an Article with ID(domain.com/..../pk/)"""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
#---------------------------
class ArticleListView(generics.ListAPIView):
    """Listing all of the Articles"""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer    
#---------------------------
    
#Categoty API views

class CategoryCreateAPIView(APIView):
    """Creating a Category"""
    def post(self, request):
        serializer = BlogCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'دسته جدید ساخته شد', 'data': serializer.data})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class CategoryDetailAPIVeiw(generics.RetrieveAPIView):
    """Getting the details of a Category with ID(domain.com/..../pk/)"""
    queryset = Category.objects.all()
    serializer_class = BlogCategorySerializer
#---------------------------
class CategoryListAPIView(generics.ListAPIView):    
    """Listing all of the Categories"""
    queryset = Category.objects.all()
    serializer_class = BlogCategorySerializer
#---------------------------
class CategoryArticlesAPIView(APIView):    
    """Listing all of the articles of one Categories"""        
    def get(self, request, category_title):
        
        try:
            category = Category.objects.get(title = category_title)
        except:
            return Response({'message': 'دسته مورد نظر وجود ندارد'}, status=status.HTTP_404_NOT_FOUND)

        articles = category.articles.all()
        serializer = ArticleSerializer(articles, many=True)
        
        return Response({'data': serializer.data})        
#---------------------------        
class CategoryUpdateAPIVeiw(generics.UpdateAPIView):
    """Updating the informations of a Category with ID(domain.com/..../pk/)"""    
    queryset = Category.objects.all()
    serializer_class = BlogCategorySerializer
#---------------------------
class CategoryDeleteAPIVew(generics.DestroyAPIView):
    """Deleting a Category with ID(domain.com/..../pk/)"""    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
#---------------------------
class LastThreeGizmologs(APIView):
    def get(self, request):
        try:
            articles = Article.objects.order_by('-publish').filter(is_for_landing=True)[ :3]
        except:
            return Response({'message': 'مقاله ای وجود ندارد'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ArticleSerializer(articles, many=True)
        return Response({'data': serializer.data})

    serializer_class = BlogCategorySerializer
#---------------------------


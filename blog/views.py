from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ArticleSerializer, CategorySerializer
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
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'دسته جدید ساخته شد', 'data': serializer.data})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class CategoryDetailAPIVeiw(generics.RetrieveAPIView):
    """Getting the details of a Category with ID(domain.com/..../pk/)"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
#---------------------------
class CategoryListAPIView(generics.ListAPIView):    
    """Listing all of the Categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
#---------------------------
class CategoryUpdateAPIVeiw(generics.UpdateAPIView):
    """Updating the informations of a Category with ID(domain.com/..../pk/)"""    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
#---------------------------
class CategoryDeleteAPIVew(generics.DestroyAPIView):
    """Deleting a Category with ID(domain.com/..../pk/)"""    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
#---------------------------
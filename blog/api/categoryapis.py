from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import  IsAdminUser
from ..serializers import *
from ..models import Category

"""
    The codes related to Categories APIs are in this file.
    Existing APIs in this file:        
        CategoryCreateAPIView --> Creates a Category object with post method
        CategoryDetailAPIView --> Gets the details of a single Category object 
        CategoryListAPIView -->  Lists all of the Category objects
        CategoryArticlesAPIView --> Lists all of the Articles of one specific Category
        CategoryUpdateAPIView --> Updates an Category objects details
        CategoryDeleteAPIView --> Deletes an Category object        
"""

class CategoryCreateAPIView(APIView):
    """
    Creating a Category
    {        
        title
        slug
        cover
        status
    }
    """
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer
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
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = BlogCategorySerializer
#---------------------------
class CategoryDeleteAPIVew(generics.DestroyAPIView):
    """Deleting a Category with ID(domain.com/..../pk/)"""    
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
#---------------------------




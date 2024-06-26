from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from .custom_permission import ArticlePostPermission
from ..serializers import *
from ..models import Article
#---------------------------
"""
    The codes related to Articles APIs are in this file.
    Existing APIs in this file:
        ArticleCreateAPIView --> Creates a single Article object with post method
        ArticleDetailAPIView --> Gets the details of a single Aritcle object 
        AritcleUpdataAPIView --> Updates an Article objects details
        ArticleDeleteAPIView --> Deletes an Article object
        ArticleListView --> Lists all of the Article objects    
        LastThreeGizmologs --> Lists the last three published Articles in GizmoLog
        PopularGizmologs --> Lists the three popular Articles in GizmoLog 
        NewsGizmologs --> Lists the five last Articles in GizmoLog 
        SimilarArticle --> Lists the five similar Articles in GizmoLog 
"""
#---------------------------
message_for_front = {
    'article_created':  'مقاله ساخته شد',
    'article_not_found' :'مقاله ای وجود ندارد'
}
#---------------------------
class ArticleCreateAPIView(APIView, ArticlePostPermission):    
    """
    Creating an Article
        {
        required:
            title 
            text 
            Author
            Cover 
            status
            slug 
            Category

        has_default:
            drafted 
            publish 
            update 
            views 
            reference_name 
            reference_link 
            is_for_landing 
        }
    """
    serializer_class = ArticleSerializer    
    permission_classes = [ArticlePostPermission]
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': message_for_front['article_created'], 'data': serializer.data})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ArticleDetailView(generics.RetrieveAPIView):
    """Getting the details of an Article with ID(domain.com/..../pk/)"""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer  
#---------------------------
class ArticleDetailSlugView(APIView):
    """Getting the details of an Article with slug(domain.com/..../slug/)""" 
    serializer_class = ArticleSerializer  
    def get(self, request,slug):
        try:
            articles = Article.objects.get(slug=slug)
        except:
            return Response({'message': message_for_front['article_not_found']}, status=status.HTTP_404_NOT_FOUND)
        
        articles.views = articles.views + 1
        articles.save()
        
        serializer = ArticleSerializer(articles)
        return Response({'data': serializer.data})      
#---------------------------
class ArticleUpdateView(generics.UpdateAPIView, ArticlePostPermission):
    """Updating the informations of an Article with ID(domain.com/..../pk/)"""
    permission_classes = [ArticlePostPermission]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer    
#---------------------------
class ArticleDeleteAPIView(generics.DestroyAPIView, ArticlePostPermission):
    """Deleting an Article with ID(domain.com/..../pk/)"""
    permission_classes = [ArticlePostPermission]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
#---------------------------
class ArticleListView(generics.ListAPIView):
    """Listing all of the Articles"""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer    
#---------------------------
class LastThreeGizmologs(APIView):
    """Lists the last three published articles in gizmo log"""    
    serializer_class = GizmoLogSerializer  
    def get(self, request):
        try:
            articles = Article.objects.order_by('-publish').filter(is_for_landing=True)[ :4]
        except:
            return Response({'message': message_for_front['article_not_found']}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GizmoLogSerializer(articles, many=True)
        return Response({'data': serializer.data})
#---------------------------
class PopularGizmologs(APIView):
    """Lists the three popular Articles in GizmoLog """  
    serializer_class = GizmoLogSerializer  
    def get(self, request):
        try:
            articles = Article.objects.order_by('-views')[ :4]
        except:
            return Response({'message': message_for_front['article_not_found']}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GizmoLogSerializer(articles, many=True)
        return Response({'data': serializer.data})
#---------------------------
class NewsGizmologs(APIView):
    """Lists the five last Articles in GizmoLog """  
    serializer_class = GizmoLogSerializer  
    def get(self, request):
        try:
            articles = Article.objects.order_by('-publish')[:5]
        except:
            return Response({'message': message_for_front['article_not_found']}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GizmoLogSerializer(articles, many=True)
        return Response({'data': serializer.data})
#---------------------------
class SimilarArticle(APIView):
    """Lists the five similar Articles in GizmoLog """  
    serializer_class = GizmoLogSerializer  
    def get(self, request,pk):
        try:
            articles = Article.objects.get(id=pk).get_similar_articles()
        except:
            return Response({'message': message_for_front['article_not_found']}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GizmoLogSerializer(articles, many=True)
        return Response({'data': serializer.data})
#---------------------------
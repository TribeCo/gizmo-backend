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
            articles = Article.objects.order_by('-publish').filter(is_for_landing=True)[ :3]
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
            articles = Article.objects.order_by('-views')[ :3]
        except:
            return Response({'message': message_for_front['article_not_found']}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GizmoLogSerializer(articles, many=True)
        return Response({'data': serializer.data})
#---------------------------
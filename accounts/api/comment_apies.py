from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import Comment,ProductComment
from blog.models import ArticleComment
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from blog.models import Article
#---------------------------
"""
    The codes related to the site's comments are in this app.
    api's in comment_apies.py :

    1- CreateCommentForArticleAPIView --> create comment for article
    2- CreateCommentForProductAPIView --> create comment for product
    3- ReadCommentForProductAPIView --> read comment for a product
    4- ReadCommentForarticleAPIView --> read comment for a article
    5- DeleteCommentAPIView --> delete comment with id
    6- UpdateCommentAPIView --> update comment with id
    

"""
#---------------------------
messages_for_front = {
    'article_not_found' : 'مقاله یافت نشد',
    'product_not_found' : 'محصول یافت نشد',
    'comment_not_found' : 'نظر یافت نشد',
    'comment_deleted' : 'نظر حذف شد',
    'comment_created' : 'نظر شما بعد از تایید ادمین نمایش داده خواهد شد.',
    'product_not_found' : 'محصول مورد نظر وجود ندارد.',
}
#---------------------------
class CreateCommentForArticleAPIView(APIView):
    """create comment for article"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ArticleCommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'messages':messages_for_front['comment_created'],'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class CreateCommentForProductAPIView(APIView):
    """create comment for product"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ProductCommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'messages':messages_for_front['comment_created'],'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------
class ReadCommentForProductAPIView(APIView):
    """read comment for a product"""
    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response({'message': messages_for_front['product_not_found']}, status=status.HTTP_404_NOT_FOUND)


        serializer = ReadCommentProductSerializer(product.comments.all(),many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#---------------------------
class ReadCommentForArticleAPIView(APIView):
    """read comment for a article"""
    def get(self, request, pk):     
        try:
            article = Article.objects.get(id=pk)
        except Article.DoesNotExist:
            return Response({'message': messages_for_front['product_not_found']}, status=status.HTTP_404_NOT_FOUND)


        serializer = ReadCommentSerializer(article.comments.all(),many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#---------------------------
class DeleteCommentAPIView(APIView):
    """delete comment with id"""
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({'message': messages_for_front['comment_not_found']}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response({'message': messages_for_front['comment_deleted']}, status=status.HTTP_204_NO_CONTENT)
#---------------------------
class UpdateCommentAPIView(APIView):
    """update comment with id"""
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({'message': messages_for_front['comment_not_found']}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------



from itertools import product
from django.db import models
from accounts.models import User
from products.models import Product
from .managers import CategoryManager, ArticleManager
from django.urls import reverse
from django.utils import timezone
from layout.utils import jalali_converter
from django.utils.html import format_html
from ckeditor.fields import RichTextField
#---------------------------
class Category(models.Model):
    status_ch = (
        ('a' , "Active"),
        ('d', "Deactive"),
    )
    title = models.CharField(max_length=50,verbose_name="تیتر")
    slug = models.SlugField(max_length=40, unique = True,verbose_name="آدرس")
    cover = models.ImageField(upload_to='media/blog/categories/%Y/%m/',null=True,blank=True,verbose_name="تصویر")
    status = models.CharField(max_length=1,choices = status_ch,verbose_name="وضعیت")

    objects = CategoryManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:category_articles",args=[self.slug,1])
        # return "comment"

    def count_articles(self):
        return self.articles.all().count()
#---------------------------
class Article(models.Model):
    status_ch = (
        ('p' , "انتشار یافته"),
        ('d', "پیش نویس"),
        ('i', "در انتظار انتشار"),
        ('b',"برگشت داده شده"),
    )
    title = models.CharField(max_length=50,verbose_name="تیتر")
    
    Author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="articles",verbose_name="نویسنده")
    cover = models.ImageField(upload_to="media/blog/articles/%Y/%m/",null=True,blank=True,verbose_name="تصویر")
    drafted = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ پیش نویس")
    publish = models.DateTimeField(default=timezone.now,verbose_name="تاریخ انتشار")
    update = models.DateTimeField(auto_now=True,verbose_name="تاریخ آپدیت")
    slug = models.SlugField(max_length=40, unique = True,verbose_name="آدرس")
    status = models.CharField(max_length=1,choices = status_ch,verbose_name="وضعیت")
    Category = models.ManyToManyField(Category,related_name = "articles",verbose_name="دسته بندی")
    views = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")

    content = RichTextField()

    read_time = models.IntegerField(default=10)

    products = models.ManyToManyField(Product,related_name="articles")

    reference_name = models.CharField(max_length=50,null=True,blank=True)
    reference_link = models.CharField(max_length=50,null=True,blank=True)

    is_for_landing = models.BooleanField(default=False)

    objects = ArticleManager()

    def preview(self):
        txtperview = self.text[:123] + " .... "
        return txtperview

    def get_absolute_url(self):
        return reverse("blog:article",args=[self.slug])

    def shamsi_date(self):
        return jalali_converter(self.publish)
    shamsi_date.short_description = "publish"

    @property
    def days_since_publish(self):
        converter = {
            "0": "۰",
            "1": "۱",
            "2": "۲",
            "3": "۳",
            "4": "۴",
            "5": "۵",
            "6": "۶",
            "7": "۷",
            "8": "۸",
            "9": "۹",
        }
        now = timezone.now()
        created_naive = timezone.make_naive(self.publish, timezone.get_default_timezone())
        created_aware = timezone.make_aware(created_naive, timezone.get_default_timezone())
        days = (now - created_aware).days
        farsi_day = converter[f"{days}"]

        return f"{farsi_day} روز پیش"

    def __str__(self):
        return f"{self.title} - {self.views}"

    def clean_text(self):
        return self.text.replace('\n', '<br>')

    def Cover_tags(self):
        return format_html("<img width=120 style='border-radius:5px' src='{}'>".format(self.Cover.url))

    def get_similar_articles(self):
        similar_articles = Article.objects.filter(Category__in=self.Category.all()).exclude(id=self.id)[:5]
        return similar_articles

    def get_comments(self):
        comments = self.comments.all()
        return comments

    def increase_views(self):
        self.views += 1
        self.save()

    @staticmethod
    def get_popular_articles():
        popular_articles = Article.objects.order_by('-views')[:5]
        return popular_articles
#---------------------------
from accounts.models import Comment
class ArticleComment(Comment):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user.full_name} - {self.article.title}"
#---------------------------

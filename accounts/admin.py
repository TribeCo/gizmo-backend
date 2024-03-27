from re import M
from django.contrib import admin
from .models import *
from blog.models import ArticleComment
#---------------------------
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(ProductComment)
admin.site.register(ArticleComment)
admin.site.register(WatchedProduct)
admin.site.register(Message)
admin.site.register(Address)
admin.site.register(DeliveryInfo)
admin.site.register(Payments)
#---------------------------


from distutils.command.upload import upload
from django.db import models
from django.urls import reverse
#---------------------------
for_what_choices = (
        ('c2' , "2col"),
        ('c3' , "3col"),
        ('b1' , "big1"),
        ('gl' , "گیزمولاگ"),
)

#---------------------------
# class ConfigShop(models.Model):
#     fname = models.CharField(max_length=200)
#     ename = models.CharField(max_length=200)
#     logo = models.ImageField(upload_to='media/config/logo/')
#     black_logo = models.ImageField(upload_to='media/config/logo/')
#     phone = models.CharField(max_length=12)
#     phone_number = models.CharField(max_length=12)
#     email = models.EmailField()
#     description = models.CharField(max_length=200)
#     insta = models.URLField()
#     whatsapp = models.URLField()
#     telegram = models.URLField()
#     aboutUs = models.TextField()
#     address = models.CharField(max_length=100)
#     color = models.CharField(max_length=6,default="82981a")
#     e_namad = models.TextField()

#     def __str__(self):
#         return f"{self.fname} - {self.ename}"
#---------------------------
# class Survey(models.Model):
#     name = models.CharField(max_length=200)
#     email = models.EmailField()
#     phoneNumber = models.CharField(max_length=200,default="None")
#     title = models.CharField(max_length=200)
#     text = models.TextField(default="None")

#     def __str__(self):
#         return f"{self.email} - {self.name}"
#--------------------------
class FAQGroup(models.Model):
     title = models.CharField(max_length=100)

     def __str__(self):
         return self.title
#---------------------------
class FAQ(models.Model):
     group = models.ForeignKey(FAQGroup,on_delete=models.CASCADE,related_name="faqs")
     question = models.CharField(max_length=100)
     answer = models.TextField()

     def __str__(self):
         return self.question
#---------------------------
class Picture(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/pictures/')

    def __str__(self):
        return self.name
#---------------------------
# class Rule(models.Model):
#     title = models.CharField(max_length=100)
#     text = models.TextField()

#     def __str__(self):
#         return self.title
#---------------------------
# class shop(models.Model):
#     name = models.CharField(max_length=100)
#     address = models.TextField()
#     postal_code = models.CharField(max_length=10)
#     phone = models.CharField(max_length=10)
#     image = models.ImageField(upload_to='media/banners/')


#     def __str__(self):
#         return self.name
#---------------------------
class Banner(models.Model): 
    name = models.CharField(max_length=100,null=True,blank=True)
    alt = models.CharField(max_length=600,null=True,blank=True) 
    image = models.ImageField(upload_to='media/banners/%Y/%m/')
    for_what = models.CharField(max_length=2,choices=for_what_choices)
    abs_link = models.CharField(max_length=200,null=True,blank=True)
    description = models.CharField(max_length=500)

    def get_absolute_url(self):
        return self.abs_link

    def __str__(self):
        return self.alt

    @staticmethod
    def filter():
        banners = Banner.objects.all()
        result = {}

        for what in for_what_choices:
            reason = what[0]
            result[reason] = banners.filter(for_what=reason)

        return result
#---------------------------
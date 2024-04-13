from django.db import models
from accounts.models import User
from products.models import Product
from layout.utils import jalali_converter
from django.utils import timezone
#---------------------------
class DubaiSites(models.Model):
    name = models.CharField(max_length=100)
    fa_name = models.CharField(max_length=100)
    website = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='media/logos/')


    def __str__(self):
        return self.name
#---------------------------
class ForeignProduct(Product):
    website = models.ForeignKey(DubaiSites,on_delete=models.CASCADE,related_name='products')
    image_link = models.CharField(max_length=500)
    product_url = models.CharField(max_length=500)
#---------------------------
class ForeignOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.Model,related_name='foreign_orders')
    name = models.CharField(max_length=300)
    link = models.URLField()
    discounted = models.BooleanField(default=False)
    discounted_price = models.IntegerField(null=True,blank=True)
    image = models.CharField(max_length=500)
    admin_checked = models.BooleanField(default=False)

    price = models.IntegerField()
    profit = models.IntegerField(default=0)

    product = models.ForeignKey(ForeignProduct,on_delete=models.Model,related_name='orders')

    tracking_code = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    derham = models.IntegerField(default=17000)
    




    def __str__(self):
        return f"{self.name} - {self.price}"

    @property
    def website_name(self):
        return self.product.website.fa_name

    @property
    def total_price(self):
        return self.price + self.profit

    @property
    def shamsi_date(self):
        return jalali_converter(self.created)

    @property
    def toman_price(self):
        return self.derham * self.price 
    
    @property
    def toman_total(self):
        return self.derham * self.total_price 

    @property
    def is_valid(self):
        delta = timezone.now() - self.updated
        if delta.total_seconds() < 24 * 60 * 60:
            return True
        else:
            return False
#---------------------------




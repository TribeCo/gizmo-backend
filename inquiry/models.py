from django.db import models
from accounts.models import User
from products.models import Product
#---------------------------
class DubaiSites(models.Model):
    name = models.CharField(max_length=100)
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
    price = models.IntegerField()
    discounted = models.BooleanField(default=False)
    discounted_price = models.IntegerField(null=True,blank=True)
    image = models.CharField(max_length=500)
    admin_checked = models.BooleanField(default=False)
    profit = models.IntegerField(default=0)
    product = models.ForeignKey(ForeignProduct,on_delete=models.Model,related_name='orders')



    def __str__(self):
        return f"{self.name} - {self.price}"
    

    def total_price(self):
        return self.price + self.profit
#---------------------------




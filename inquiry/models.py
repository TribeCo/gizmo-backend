from django.db import models
from accounts.models import User
#---------------------------
class ForeignOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.Model)
    name = models.CharField(max_length=300)
    link = models.URLField()
    price = models.IntegerField()
    discounted = models.BooleanField(default=False)
    discounted_price = models.IntegerField(null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    admin_checked = models.BooleanField(default=False)
    profit = models.IntegerField(default=0)



    def __str__(self):
        return f"{self.name} - {self.price}"
    

    def total_price(self):
        return self.price + self.profit
#---------------------------
class DubaiSites(models.Model):
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='media/logos/')


    def __str__(self):
        return self.name
#---------------------------
from products.models import Product

class ForeignProduct(Product):
    class Meta:
        proxy = True
        exclude = ['price',]
    
    website = models.ForeignKey(DubaiSites,on_delete=models.CASCADE,related_name='products')
#---------------------------


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


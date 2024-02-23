from django.db import models
from products.models import Product 
from accounts.models import User
#---------------------------
def formatPay(pay):
    return "{:,.0f}".format(pay)
#---------------------------
class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='cart')
    
    def __str__(self):
        return f'{self.user} - {self.id}'

    def get_total_price(self):
        return formatPay(self.total_price())

    def total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount/100)* total
            return total - discount_price
        return total

    def tax(self):
        return 9 * self.total_price() / 100
    
    def get_tax(self):
        return formatPay(9 * self.total_price() / 100)

    def taxAndTotal(self):
        return formatPay(self.total_price() + self.tax())
#---------------------------
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='cart_items')
    price = models.IntegerField()
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.product.discounted_price_int * self.quantity

    def get_cost_from_product(self):
        return format(self.product.discounted_price_int * self.quantity)
#---------------------------
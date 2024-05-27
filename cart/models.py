from django.db import models
from products.models import Color, Product 
from accounts.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
#---------------------------
def formatPay(pay):
    return "{:,.0f}".format(pay)
#---------------------------
class Coupon(models.Model):
    code = models.CharField(max_length=30,unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    users = models.ManyToManyField(User,blank=True)

    def __str__(self):
        return f"{self.discount}-{self.code}"

    def is_valid(self):
        now = timezone.now().date()
        return self.valid_from <= now <= self.valid_to
#---------------------------
class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='cart')
    discount = models.IntegerField(blank=True,null=True,default=None)
    coupon = models.ForeignKey(Coupon,blank=True,null=True,default=None,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.id}'

    @property
    def get_total_price(self):
        return formatPay(self.total_price())

    def total_price(self):
        total = sum(item.get_total_cost() for item in self.items.all())
        return total
    
    def total_discounted_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.coupon:
            discount_price = (self.coupon.discount/100) * total
            return total - discount_price
        return total
    
    def delta_discounted(self):
        return (self.total_price() - self.total_discounted_price())

    def get_discount_coupon(self):
        if self.coupon:
            return self.coupon.discount
        return 0

    def remove_coupon(self,user):
        if(self.coupon):
            self.coupon.users.remove(user)
            self.discount = 0
            self.coupon = None
            self.save()

    def tax(self):
        return 9 * self.total_discounted_price() / 100
    
    def get_tax(self):
        return formatPay(9 * self.total_discounted_price() / 100)

    def taxAndTotal(self):
        return formatPay(self.total_discounted_price() + self.tax())
#---------------------------
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='cart_items')
    price = models.IntegerField()
    quantity = models.PositiveSmallIntegerField(default=1)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    is_sync = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    def get_total_cost(self):
        return self.product.price * self.quantity

    def get_cost(self):
        return self.product.discounted_price_int * self.quantity

    def get_cost_from_product(self):
        return format(self.product.discounted_price_int * self.quantity)
#---------------------------
class TempCart(models.Model):
    discount = models.IntegerField(blank=True,null=True,default=None)
    coupon = models.ForeignKey(Coupon,blank=True,null=True,default=None,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'

    @property
    def get_total_price(self):
        return formatPay(self.total_price())

    def total_price(self):
        return sum(item.get_total_cost() for item in self.temp_items.all())
    
    def total_discounted_price(self):
        return sum(item.get_cost() for item in self.temp_items.all())
    
    def delta_discounted(self):
        return (self.total_price() - self.total_discounted_price())

    def tax(self):
        return 9 * self.total_price() / 100
    
    def get_tax(self):
        return formatPay(9 * self.total_price() / 100)

    def taxAndTotal(self):
        return formatPay(self.total_price() + self.tax())
#---------------------------
class TempCartItem(models.Model):
    cart = models.ForeignKey(TempCart,on_delete=models.CASCADE,related_name='temp_items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.PositiveSmallIntegerField(default=1)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.product.discounted_price_int * self.quantity
    
    def get_total_cost(self):
        return self.product.price * self.quantity

    def get_cost_from_product(self):
        return format(self.product.discounted_price_int * self.quantity)
#---------------------------


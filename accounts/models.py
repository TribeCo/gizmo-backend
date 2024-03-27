from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from products.models import Product
from .managers import MyUserManager
from layout.utils import jalali_converter_with_hour,jalali_converter
import uuid
#---------------------------
delivery_methods = (
        ('c' , "درون شهری"),
        ('b' , "اتوبوس"),
        ('p', "پست معمولی"),
        ('t',"تیپاکس (پس کرایه)"),
    )
gender_options = (
        ('m' , "آقا"),
        ('f' , "خانم"),
        ('u', "ترجیح میدم نگویم."),
    )
#---------------------------
class ProfileUser(models.Model):
    image = models.ImageField(upload_to='media/users/%Y/%m/')
    bio = models.CharField(max_length=500)

    def __str__(self):
        return str(self.bio)
#---------------------------
class DeliveryInfo(models.Model):
    name_delivery = models.CharField(max_length=50)
    phone_delivery = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    delivery_method = models.CharField(max_length=1,choices = delivery_methods,default='p')

    def __str__(self):
        return str(self.name_delivery)
#---------------------------
class User(AbstractBaseUser):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phoneNumber = models.CharField(unique=True, max_length=11)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    profile = models.OneToOneField(ProfileUser,on_delete=models.SET_NULL,blank=True,null=True,related_name="user") 
    delivery_info = models.OneToOneField(DeliveryInfo,on_delete=models.SET_NULL,blank=True,null=True,related_name="user") 
    

    can_change_password = models.BooleanField(default=False)

    birthday = models.DateField(blank=True,null=True)


    code = models.IntegerField(blank=True,null=True)


    wishlist = models.ManyToManyField(Product,blank=True,related_name ="wishlist")
    informing = models.ManyToManyField(Product,blank=True,related_name ="informing")

    gender = models.CharField(max_length=1,choices = gender_options,default='u')



    USERNAME_FIELD = 'phoneNumber'
    objects = MyUserManager()

    def __str__(self):
        return str(self.phoneNumber) + " - " + str(self.full_name)+ " - " + str(self.id)

    def blog_articles(self):
        return reverse("blog:author_articles",args=[1,self.id])

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def change_current_address(self,pk):
        for ad in self.addresses.all():
            ad.current = False
            ad.save()
        address = self.addresses.get(id=pk)
        address.current = True
        address.save()

    def total_price(self):
        return self.cart.total_price()

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def birth_day(self):
        return jalali_converter(self.birthday) 

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
#---------------------------
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    straight_address = models.TextField()
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20,blank=True,null=True)
    current = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + " - " + str(self.postal_code)

#---------------------------
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(default=False)

    rating = models.FloatField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_comments', blank=True)

    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    anonymous = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.full_name}"

    def star_rating(self):
        return self.rating * 20

    def shamsi_date(self):
        return jalali_converter_with_hour(self.created) 
    
    @property
    def days_since_creation(self):
        now = timezone.now()
        created_naive = timezone.make_naive(self.created, timezone.get_default_timezone())
        created_aware = timezone.make_aware(created_naive, timezone.get_default_timezone())
        days = (now - created_aware).days
        return f"{days} روز پیش"
#---------------------------
class ProductComment(Comment):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user.full_name} - {self.product.name}"
#---------------------------
class WatchedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="wacthed")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.product.name} - {self.timestamp}"
#---------------------------
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    title = models.CharField(max_length=100)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    abs_link = models.CharField(max_length=200)


    def __str__(self):
        return f"{self.title}-{self.user.full_name}"

    @property
    def shamsi_date(self):
        return jalali_converter(self.created) 
    
    def days_since_creation(self):
        now = timezone.now()
        created_naive = timezone.make_naive(self.created, timezone.get_default_timezone())
        created_aware = timezone.make_aware(created_naive, timezone.get_default_timezone())
        days = (now - created_aware).days
        return f"{days} روز پیش"
#---------------------------
class Payments(models.Model):
    ref_id = models.CharField(max_length=100,null=True,blank=True)
    authority = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="payments")
    amount = models.IntegerField()


    def __str__(self):
        return str(self.user) + " - " + str(self.amount)
#---------------------------

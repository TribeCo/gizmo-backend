from tokenize import Special
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor.fields import RichTextField
#---------------------------
class Brand(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True, allow_unicode=True)
    logo = models.ImageField(upload_to='media/logos/')
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    website = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.name.replace(" ","-")
        super(Brand, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('stuff:product_detail',args=[self.slug,self.id])

#---------------------------
class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE, related_name='scategory',null=True,blank=True)
    is_sub = models.BooleanField(default=False)
    is_for_landing = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/categories/',blank=True,null=True)
    slug = models.SlugField(max_length=200,unique=True, allow_unicode=True)
    color = models.CharField(max_length=10,blank=True,null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    @property
    def type(self):
        return "category"

    def get_absolute_url(self):
        return reverse('stuff:category_detail',args=[self.id,1])

    def save(self, *args, **kwargs):
        self.slug = self.name.replace(" ","-")
        super(Category, self).save(*args, **kwargs)
#--------------------------- 
class Tags(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,related_name = 'tags',on_delete = models.CASCADE,blank=True,null=True)
    
    def __str__(self):
        return self.name
           
#---------------------------
class Color(models.Model):
    name = models.CharField(max_length=50)
    en = models.CharField(max_length=50)
    code = models.CharField(max_length=6)

    def __str__(self):
        return self.name
#---------------------------
class ProductManager(models.Manager):
    def are_available(self):
        products = self.all()
        products_ids = [o.id for o in products if o.is_available]
        products_filtered = products.filter(id__in=products_ids)
        return products_filtered
#---------------------------
class Product(models.Model):
    category = models.ManyToManyField(Category,related_name='products',blank=True)
    brand = models.ForeignKey(Brand,related_name='products',null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    En = models.CharField(max_length=200,blank=True,null=True) 
    slug = models.SlugField(max_length=200,unique=True, allow_unicode=True)
    
    price = models.IntegerField()
    
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])

    ordered = models.IntegerField(default=0)

    send_free = models.BooleanField(default=False)
    net_sale = models.BooleanField(default=False)


    content = RichTextField()


    code = models.CharField(max_length=10,blank=True,null=True)

    image1 = models.ImageField(upload_to='media/products/%Y/%m/')
    image2 = models.ImageField(upload_to='media/products/%Y/%m/')
    special_image = models.ImageField(upload_to='media/products/%Y/%m/')
    alt = models.CharField(max_length=200)



    discount = models.IntegerField(default=0)
    discounted = models.BooleanField(default=False)

    objects = ProductManager()

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('stuff:product_detail',args=[self.slug,self.id])
    
    def update_warehouse(self,color_id,amount=1):
        product_color_object = self.product_color.get(color__id=color_id)
        
        product_color_object.quantity = product_color_object.quantity - amount

        if(product_color_object.quantity == 0):
            product_color_object.available = False   
    
        product_color_object.save()
        self.ordered = self.ordered + amount
        self.save()

    def get_brand_name(self):
        return self.brand.name

    @property
    def discounted_price(self):
        show = int(((self.price)*(100-self.discount))/100)
        formatted_price = "{:,.0f}".format(show)
        return formatted_price
        
    def dubai_product(self):
        return False
    
    @property
    def is_available(self):
        return self.warehouse > 0
    
    @property
    def type(self):
        return "product"

    @property
    def warehouse(self):
        pcolors = self.product_color.all() 

        total = 0
        for pcolor in pcolors:
            total += pcolor.quantity

        return total
        
    @property
    def discounted_price_int(self):
        show = int(((self.price)*(100-self.discount))/100)
        return show

    @property
    def comment_count(self):
        return self.comments.all().count()
    
    def get_comments(self):
        comments = self.comments.all().filter(valid=True)
        return comments

    def ordered_increase(self,amount):
        self.ordered += 1
        return True

    @property
    def is_new(self):
        return True if(timezone.now().day - self.updated.day <= 4) else False

    def __str__(self):
        return self.name

    def star_rating(self):
        return self.rating * 20

    def clean_short_description(self):
        return self.short_description.replace('\n', '<br>')

    def clean_description(self):
        return self.description.replace('\n', '<br>')
    
    def clean_more_info(self):
        return self.more_info.replace('\n', '<br>')

    def get_most_color(self):
        colors = sorted(self.product_color.all(), key=lambda x: x.quantity, reverse=True)
        return colors[0].color.id


    def get_similar_products(self):
        product_ids = []
        for category in self.category.all():
            product_ids.extend(category.products.are_available().exclude(id=self.id).values_list('id', flat=True)[:6])
            product_ids.extend(Product.objects.are_available().exclude(id=self.id).values_list('id', flat=True))
                
        # remain = 6 - len(product_ids)
        # while(remain > 0):
        
        #     product_ids = list(set(product_ids))    
        #     remain = 6 - len(product_ids)            
        #product_ids = product_ids[:6]

        similar_products = Product.objects.filter(id__in=product_ids).distinct()

        return similar_products
#---------------------------
class ProductColor(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_color')
    color = models.ForeignKey(Color,on_delete=models.CASCADE,related_name='product_color')
    quantity = models.IntegerField()
    available = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.product}-{self.color}-{self.quantity}"
        
    
#---------------------------
class ProductImage(models.Model):
    image = models.ImageField(upload_to='media/products/%Y/%m/')
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='images',null=True,blank=True)
    alt = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.product} - {self.id}"
#---------------------------
class Attribute(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='attributes',null=True,blank=True)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product} - {self.id}"
#---------------------------

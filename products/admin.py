from django.contrib import admin
from .models import *
#---------------------------
class AttributeItemInline(admin.TabularInline):
    model = Attribute
    raw_id_fields = ('product',)
    fields = ('key', 'value','is_main')
#---------------------------
class ProductImageItemInline(admin.TabularInline):
    model = ProductImage
    raw_id_fields = ('product',)
    fields = ('alt', 'image')
#---------------------------
class ProductColorInline(admin.TabularInline):
    model = ProductColor
    raw_id_fields = ('product',)
    fields = ('quantity','color')
#---------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','updated','is_new','id')
    search_fields = ['name', 'description',]
    prepopulated_fields = {'slug':('name',)}
    list_filter = ('created',)
    list_editable = ('price',)
    raw_id_fields = ('category',)
    actions = ('make_available','make_unavailable','add_specific_color')
    inlines = (ProductImageItemInline,AttributeItemInline,ProductColorInline)

    def make_available(self,request,queryset):
        rows = queryset.update(is_available=True)
        self.message_user(request,f'{rows} updated')

    def make_unavailable(self,request,queryset):
        rows = queryset.update(is_available=False)
        self.message_user(request,f'{rows} updated')


    make_available.short_description = 'make all available'
#---------------------------
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(ProductColor)
admin.site.register(Brand)
#---------------------------
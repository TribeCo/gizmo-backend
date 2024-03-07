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
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','available','updated','is_new')
    search_fields = ['name', 'description',]
    prepopulated_fields = {'slug':('name',)}
    list_filter = ('available','created')
    list_editable = ('price',)
    raw_id_fields = ('category',)
    actions = ('make_available','make_unavailable','add_specific_color')
    inlines = (ProductImageItemInline,AttributeItemInline)

    def make_available(self,request,queryset):
        rows = queryset.update(available=True)
        self.message_user(request,f'{rows} updated')

    def make_unavailable(self,request,queryset):
        rows = queryset.update(available=False)
        self.message_user(request,f'{rows} updated')

    def add_specific_color(self, request, queryset):
        color = Color.objects.get(en='custom')
        for product in queryset:
            product.colors.add(color)
        self.message_user(request, f'The specific color has been added to selected products.')


    make_available.short_description = 'make all available'
    add_specific_color.short_description = 'Add specific color to selected products'
#---------------------------
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Brand)
#---------------------------
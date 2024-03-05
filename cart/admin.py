from django.contrib import admin
from .models import Cart, CartItem, Coupon
#---------------------------
admin.site.register(Coupon)
admin.site.register(CartItem)
#---------------------------
class CartItemImageItemInline(admin.TabularInline):
    model = CartItem
    # raw_id_fields = ('product',)
    # fields = ('alt', 'is_main','image','image_tag')
    # readonly_fields = ('image_tag',)
#---------------------------
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    # list_display = ('name','image_tag','price','available','updated','is_new')
    # search_fields = ['name', 'description',]
    # prepopulated_fields = {'slug':('name',)}
    # list_filter = ('available','created')
    # list_editable = ('price',)
    # raw_id_fields = ('category',)
    # actions = ('make_available','make_unavailable','add_specific_color')
    inlines = (CartItemImageItemInline,)

#-------------------------------------------------------------------------
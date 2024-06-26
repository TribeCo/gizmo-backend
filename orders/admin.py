from django.contrib import admin

from accounts.models import Payments
from .models import *

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)
#---------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','created','updated','paid')
    list_filter = ('paid',)
    inlines = (OrderItemInline,)
#---------------------------


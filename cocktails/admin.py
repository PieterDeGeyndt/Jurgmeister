from ast import If
from django.contrib import admin
from .models import BillingAddress, Cocktails, OrderItem, Order, Payment

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','ordered','start_date','delivery_method']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item','quantity','ordered','user','ordered_timestamp']
    
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','timestamp']    

admin.site.register(Cocktails)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(BillingAddress)
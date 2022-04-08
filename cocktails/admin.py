from django.contrib import admin
from .models import Cocktails, OrderItem, Order, Payment

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','ordered']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item','user']

admin.site.register(Cocktails)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)



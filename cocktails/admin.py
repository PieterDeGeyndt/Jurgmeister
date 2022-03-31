from django.contrib import admin
from .models import Cocktails, OrderItem, Order, Payment

admin.site.register(Cocktails)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Payment)



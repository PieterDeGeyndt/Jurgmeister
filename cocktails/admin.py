from django.contrib import admin
from .models import Cocktails, OrderItem, Order

admin.site.register(Cocktails)
admin.site.register(OrderItem)
admin.site.register(Order)



from ast import If
from django.contrib import admin
from .models import BillingAddress, Cocktails, OrderItem, Order, Payment

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','orderid','ordered','delivery_method','mollie_id','start_date']
    
    def get_object(self, request, object_id, s):
        # Hook obj for use in formfield_for_manytomany
        self.obj = super(OrderAdmin, self).get_object(request, object_id)
        # print ("Got object:", self.obj)
        return self.obj

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "items":
            kwargs["queryset"] = OrderItem.objects.filter(order=self.obj)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item','quantity','ordered','user','ordered_timestamp']
    
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','order_id', 'mollie_payment_id','status','timestamp']

admin.site.register(Cocktails)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(BillingAddress)
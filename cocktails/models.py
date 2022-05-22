from datetime import datetime
from unittest.util import _MAX_LENGTH
from django.db import models
from django.conf import settings
import uuid

CATEGORY_CHOICES=(
    ('M', 'Mocktails'),
    ('C', 'Cocktails'),
)

class Cocktails(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='cocktails/')
    body = models.TextField()
    category = models.CharField(default="C",choices=CATEGORY_CHOICES, max_length=1)
    pubdate = models.DateTimeField(auto_now_add=True)
    garnish = models.TextField(blank=True)
    taste = models.TextField(blank=True)
    price = models.FloatField(default=10.00)
    discount_price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:200]

class OrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, 
                            on_delete=models.CASCADE, blank=True, null = True)
    ordered=models.BooleanField(default=False)
    item=models.ForeignKey(Cocktails, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    ordered_timestamp = models.DateTimeField(blank=True,null = True)

    def __str__(self):
            template='{0.quantity} x {0.item}'
            return template.format(self)
    
    def get_total_item_price(self):
        return self.quantity * self.item.price
    
    def get_total_discount_price(self):
        return self.quantity * self.item.discount_price
    
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_price()
    
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        return self.get_total_item_price()

class Order(models.Model):
    orderid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                            on_delete=models.CASCADE)
    start_date=models.DateTimeField()
    ordered_date = models.DateTimeField(default=datetime.now())
    ordered=models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    delivery_method = models.CharField(max_length=1, null=True,blank=True)
    billing_address=models.ForeignKey('BillingAddress',on_delete=models.SET_NULL, blank=True, null=True)
    charge=models.ForeignKey('Payment',on_delete=models.SET_NULL, blank=True, null=True)
    total = models.FloatField(default=0.00)

    def __str__(self):
        template='ID: {0.orderid} - Ordered by: {0.user.username} - Totaal: €{0.total}'
        return template.format(self)

    def get_total(self):
        total=0.00
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
    
    def get_total_delivery(self):
        total=5.00
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

class BillingAddress(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=14)
    street_address = models.CharField(max_length=100)
    appartment_address=models.CharField(max_length=100)
    zip=models.CharField(max_length=100)
    adult=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    mollie_payment_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField()
    link = models.TextField(blank=True, null=True)
    ordered= models.ManyToManyField(OrderItem,blank=True)

    def __str__(self):
        return self.user.username
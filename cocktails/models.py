from django.db import models
from django.conf import settings

CATEGORY_CHOICES=(
    ('M', 'Mocktails'),
    ('C', 'Cocktails'),
)

class Cocktails(models.Model):
    title = models.CharField(max_length=255)
    pubdate = models.DateTimeField()
    body = models.TextField()
    image = models.ImageField(upload_to='cocktails/')
    garnish = models.TextField(default="garnishes")
    taste = models.TextField(default="sweetsour")
    price = models.FloatField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:200]

class OrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, 
                            on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    item=models.ForeignKey(Cocktails, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def __str__(self):
            template='{0.item} {0.quantity}'
            return template.format(self)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                            on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
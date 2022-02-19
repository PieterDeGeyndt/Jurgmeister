from django.db import models

class Services(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=200)
    body = models.TextField(default="Dit is fake bodytext, vervang mij in de admin")
    quotes= models.TextField(default="Dit is fake quotetext, vervang mij in de admin")

    def __str__(self):
        return self.title
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Product(models.Model):
    categories = models.ManyToManyField(Category)
    name = models.CharField(max_length=30)
    details = models.TextField(blank=True)
    description = models.CharField(max_length=30)
    image_url = models.CharField(max_length=400, default="https://i.stack.imgur.com/y9DpT.jpg")
    price = models.FloatField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    totalPrice = models.FloatField()

    def total_price(self):
        queryset = self.products.all().aggregate(
        total_price=models.Sum('price'))
        return queryset["total_price"]
    


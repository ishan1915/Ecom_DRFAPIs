from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email=models.EmailField(blank=False)
    is_seller = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_seller': True})
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # New field

    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_seller': False})
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    ordered_at = models.DateTimeField(auto_now_add=True)


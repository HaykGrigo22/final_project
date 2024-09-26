from audioop import reverse

from django.contrib.auth import get_user_model
from django.db import models

from category.models import Category
from helper.storage import upload_product_image, upload_producer_logo_image
from helper.validators import valid_price
from producer.models import Producer


User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=155)
    price = models.FloatField(validators=[valid_price])
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, null=True, blank=True, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()
    year = models.IntegerField()
    image = models.ImageField(upload_to=upload_product_image, null=True, blank=True)

    def __str__(self):
        return f"{self.producer} : {self.name}"


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}"


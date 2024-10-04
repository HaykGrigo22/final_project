from django.db import models

from helper.storage import upload_category_image


class Category(models.Model):
    name = models.CharField(max_length=155)
    image = models.ImageField(upload_to=upload_category_image, null=True, blank=True)
    description = models.CharField(max_length=525, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

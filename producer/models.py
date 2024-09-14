from audioop import reverse

from django.db import models

from category.models import Category
from helper.storage import upload_producer_logo_image


# User = get_user_model()


class Producer(models.Model):
    producer_name = models.CharField(max_length=155)
    description = models.TextField()
    logo = models.ImageField(upload_to=upload_producer_logo_image, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='producers', null=True, blank=True)
    # creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("producer", kwargs={"pk": self.pk})

    def __str__(self):
        return self.producer_name

    class Meta:
        verbose_name = "Producer"
        verbose_name_plural = "Producers"

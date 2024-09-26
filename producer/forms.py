from django import forms

from home.models import Product
from producer.models import Producer


class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = ['producer_name', 'description', 'logo', 'categories']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "producer", "category", "description", "year", "image"]


ProductFormSet = forms.inlineformset_factory(
    Producer, Product, form=ProductForm, extra=1, can_delete=True
)

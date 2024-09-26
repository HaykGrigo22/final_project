from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from category.models import Category
from home.models import Product


class CategoryListView(ListView):
    model = Category
    template_name = "category/categories.html"
    context_object_name = 'categories'
    queryset = Category.objects.all()


class CategoryDetailView(DetailView):
    model = Category
    template_name = "category/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["products"] = Product.objects.filter(category__id=self.object.id)

        return context


class CategoryProducerView(TemplateView):
    template_name = "category/producer_category.html"

    def get_context_data(self, producer_id, category_id, **kwargs):
        context = super().get_context_data(**kwargs)

        context["products"] = Product.objects.filter(category__id=category_id, producer__id=producer_id)

        return context

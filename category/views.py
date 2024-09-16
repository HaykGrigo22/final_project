from django.views.generic import ListView, DetailView

from category.models import Category


class CategoryListView(ListView):
    model = Category
    template_name = "category/categories.html"
    context_object_name = 'categories'
    queryset = Category.objects.all()


class CategoryDetailView(DetailView):
    model = Category
    template_name = "category/category_detail.html"
    context_object_name = 'category'


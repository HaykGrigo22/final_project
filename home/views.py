from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from basket.models import Basket
from home.models import Product, WishList


class HomeListView(ListView):
    model = Product
    template_name = "home/home.html"
    context_object_name = 'products'
    queryset = Product.objects.all()


class ProductDetailView(DetailView):
    model = Product
    template_name = "home/product_detail.html"
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context["similar_product_by_producer"] = (Product.objects.filter(producer=product.producer).
                                                  exclude(id=product.id))
        return context


class AboutUsView(TemplateView):
    template_name = "home/about_us.html"


class WishListAddView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        wish_list = WishList.objects.filter(user=request.user, product=product)

        if not wish_list.exists():
            WishList.objects.create(user=request.user, product=product)

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class AdvancedSearchView(TemplateView):
    template_name = "home/advanced_search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        producer = self.request.GET.get("producer")
        category = self.request.GET.get("category")
        description = self.request.GET.get("description")

        all_products = Product.objects.all()

        search_list = []

        if name:
            search_list.append(Q(name__icontains=name))
        if producer:
            search_list.append(Q(producer__icontains=producer))
        if min_price:
            search_list.append(Q(price__gte=min_price))
        if max_price:
            search_list.append(Q(price__lte=max_price))
        if description:
            search_list.append(Q(description__icontains=description))
        if description:
            search_list.append(Q(category__icontains=category))

        for condition in search_list:
            all_products = all_products.filter(condition)

            context["products"] = all_products

        return context


class WishListView(ListView):
    model = WishList
    template_name = "home/wish_list.html"
    context_object_name = 'wish_list'
    queryset = WishList.objects.all()

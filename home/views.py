from django.views.generic import ListView, DetailView, TemplateView

from home.models import Product


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

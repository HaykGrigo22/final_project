from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from category.models import Category
from home.forms import ProductForm
from home.models import Product, WishList
from producer.models import Producer


class HomeListView(ListView):
    model = Product
    template_name = "home/home.html"
    context_object_name = 'products'
    queryset = Product.objects.all().order_by('name')
    paginate_by = 3


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = {
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image': product.image.url,
    }
    return JsonResponse(data)


class ProductDetailView(DetailView):
    model = Product
    template_name = "home/product_detail.html"
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        request = self.request

        if request.GET.get("producer"):
            context["similar_products"] = (Product.objects.filter(producer=product.producer, category=product.category).
                                           exclude(id=product.id))
        elif request.GET.get("category"):
            context["similar_products"] = (Product.objects.filter(category=product.category).
                                           exclude(id=product.id))
        elif request.GET.get("price"):
            context["similar_products"] = (
                Product.objects.filter(
                    Q(price__gte=product.price - 20) & Q(price__lte=product.price + 20) & Q(category=product.category)).
                exclude(id=product.id))

        else:
            context["similar_products"] = Product.objects.filter(

                Q(producer=product.producer, category=product.category) |

                Q(category=product.category) |

                (Q(price__gte=product.price - 5) & Q(price__lte=product.price + 5) & Q(category=product.category))

            ).exclude(id=product.id)
        # context["similar_product_by_producer"] = (Product.objects.filter(producer=product.producer).
        #                                           exclude(id=product.id))

        return context


class AboutUsView(TemplateView):
    template_name = "home/about_us.html"


class ModalView(TemplateView):
    template_name = "home/modal.html"


class WishListAddView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        wish_list = WishList.objects.filter(user=request.user, product=product)

        if not wish_list.exists():
            WishList.objects.create(user=request.user, product=product)

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class RemoveFromWishListView(LoginRequiredMixin, View):
    def post(self, request, wish_item_id):
        wish_item = get_object_or_404(WishList, id=wish_item_id, user=request.user)

        wish_item.delete()

        return redirect('home:wish_list')


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
            search_list.append(Q(producer__id=producer))
        if min_price:
            search_list.append(Q(price__gte=min_price))
        if max_price:
            search_list.append(Q(price__lte=max_price))
        if description:
            search_list.append(Q(description__icontains=description))
        if category:
            search_list.append(Q(category__id=category))

        if search_list:
            all_products = all_products.filter(*search_list)

        context["products"] = all_products

        context["producers"] = Producer.objects.all()
        context["categories"] = Category.objects.all()

        return context


class WishListView(TemplateView):
    template_name = "home/wish_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["wish_list_products"] = WishList.objects.filter(user=self.request.user)

        return context


class AddProductView(CreateView):
    model = Product
    fields = ["name", "price", "producer", "category", "description", "year", "image"]
    template_name = "home/add_product.html"

    def get_success_url(self):
        return reverse('home:home')


class SearchView(ListView):
    model = Product
    template_name = "home/search.html"
    context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get('search')
        object_list = Product.objects.none()
        if query:
            object_list = Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        return object_list


class UpdateProductView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "home/update_product.html"

    def get_success_url(self):
        return reverse_lazy("home:product_detail",
                            kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        return super().get_object(queryset)


class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'home/delete_product.html'
    success_url = reverse_lazy('home:home')

    def get_object(self, queryset=None):
        return super().get_object(queryset)


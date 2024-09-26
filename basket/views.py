from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Sum, F

from basket.models import Basket
from home.models import Product


class BasketAddView(View):

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        current_page = request.META.get("HTTP_REFERER")

        basket = request.session.get('basket', {})

        if str(product_id) in basket:
            basket[str(product_id)]["quantity"] += 1
        else:
            basket[str(product_id)] = {
                "id": product.id,
                "product_title": product.name,
                "quantity": 1,
                "price": float(product.price),
                "image": product.image.url
            }

        request.session['basket'] = basket

        return HttpResponseRedirect(current_page)


class UserBasketView(TemplateView):
    template_name = "users/basket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        basket = self.request.session.get("basket", {})
        total_sum = 0

        basket_items = []
        for item in basket.values():
            product = Product.objects.get(pk=item["id"])
            basket_items.append({
                "product": product,
                "quantity": item['quantity']
            })
            total_sum += product.price * item['quantity']

        context["baskets"] = basket_items
        context["total_sum"] = total_sum

        return context


class BasketDeleteView(View):
    def get(self, request, product_id):

        basket = request.session.get("basket", {})
        if str(product_id) in basket:
            del basket[str(product_id)]
            request.session["basket"] = basket

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class BasketQuantityArrowUpView(View):
    def get(self, request, product_id):
        basket = request.session.get("basket", {})

        if str(product_id) in basket:
            basket[str(product_id)]["quantity"] += 1
        else:
            raise Http404("Product not found in the basket")

        request.session["basket"] = basket

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", '/'))


class BasketQuantityArrowDownView(View):
    def get(self, request, product_id):
        basket = request.session.get("basket", {})

        if str(product_id) in basket:
            if basket[str(product_id)]["quantity"] > 1:
                basket[str(product_id)]["quantity"] -= 1
        else:
            raise Http404("Product not found in the basket")

        request.session["basket"] = basket

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", '/'))

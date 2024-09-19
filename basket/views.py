from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from basket.models import Basket
from home.models import Product


class BasketAddView(View):

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        current_page = request.META.get("HTTP_REFERER")

        if request.user.is_authenticated:
            basket, created = Basket.objects.get_or_create(user=request.user, product=product)

            if not created:
                basket.quantity += 1
                basket.save()
        else:
            basket = request.session.get('basket', {})

            if str(product_id) in basket:
                basket[str(product_id)]["quantity"] += 1
            else:
                basket[str(product_id)] = {
                    "id": product.id,
                    "product_title": product.name,
                    "quantity": 1,
                    "price": product.price,
                    "image": product.image.url
                }

            request.session['basket'] = basket

        return HttpResponseRedirect(current_page)


class UserBasketView(TemplateView):
    template_name = "users/basket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            basket = Basket.objects.filter(user=self.request.user)
            total_sum = sum(item.product.price * item.quantity for item in basket)
            context['baskets'] = basket
        else:
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

            context['baskets'] = basket_items

        context['total_sum'] = total_sum

        return context


class BasketDeleteView(View):
    def get(self, request, product_id):
        if request.user.is_authenticated:
            basket_item = get_object_or_404(Basket, product_id=product_id, user=request.user)
            basket_item.delete()
        else:
            basket = request.session.get("basket", {})
            if str(product_id) in basket:
                del basket[str(product_id)]
                request.session["basket"] = basket

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

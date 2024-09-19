from django.urls import path
from basket import views


app_name = "basket"

urlpatterns = [
    path("my-basket/", views.UserBasketView.as_view(), name="basket"),
    path("basket-add/<int:product_id>/", views.BasketAddView.as_view(), name="basket_add"),
    path("basket-delete/<int:product_id>/", views.BasketDeleteView.as_view(), name="basket_delete"),
]



from django.urls import path
from home.api import views

app_name = "api"

urlpatterns = [
    path("api/v1/home/", views.HomeListAPIView.as_view(), name="api_home"),
    path("api/v1/product-crud/<int:pk>/", views.ProductUpdateDeleteGetAPIView.as_view(), name="api_product_detail"),
    path("api/v1/product-create/", views.ProductCreateAPIView.as_view(), name="api_product_detail"),

    path("api/v1/user-logout/", views.LogoutAPIView.as_view(), name="api_logout_user"),

    path("api/v1/categories/", views.CategoryListAPIView.as_view(), name="api_categories"),
    path("api/v1/category-detail/<int:pk>/", views.CategoryDetailAPIView.as_view(), name="api_category_detail"),
    path("api/v1/producer-category/<int:producer_id>/<int:category_id>/", views.CategoryProducerAPIView.as_view(),
         name="api_producer_category"),

    path("api/v1/producers/", views.ProducerListAPIView.as_view(), name="api_producers"),
    path("api/v1/producer-detail/<int:pk>/", views.ProducerDetailAPIView.as_view(), name="api_producer_detail"),
    path("api/v1/producer-create-with-products/", views.ProducerCreateAPIView.as_view(),
         name="api_producers_creation_with_product"),

    path("api/v1/about-us/", views.AboutUsAPIView.as_view(), name="api_about_us"),

    path("api/v1/search/", views.SearchAPIView.as_view(), name="api_search"),
    path("api/advanced-search/", views.AdvancedSearchAPIView.as_view(), name="api_advanced_search"),

    path("api/v1/user-profile/", views.UserProfileGetUpdateAPIView.as_view(), name="api_user_profile"),

    path("api/v1/wish-list/", views.WishListAPIView.as_view(), name="wish_list_api"),
    path("api/v1/wish-list/delete/<int:product_id>/", views.WishListItemDeleteAPIView.as_view(),
         name="api_wish_list_delete"),
    path("api/v1/wish-list/add/<int:product_id>/", views.WishListItemADdAPIView.as_view(), name="ai_wish_list_add"),

    path("api/v1/user-basket/", views.UserBasketAPIView.as_view(), name="api_user_basket"),
    path("api/v1/product-add-to-basket/<int:product_id>/", views.BasketAddAPIView.as_view(), name="api_basket_add"),
    path("api/v1/product-delete-from-basket/<int:product_id>/", views.BasketDeleteAPIView.as_view(),
         name="api_basket_delete"),
    path("api/v1/basket-product/quantity-up/<int:product_id>/", views.BasketQuantityArrowUpAPIView.as_view(),
         name="api_arrow_up"),
    path("api/v1/basket-product/quantity-down/<int:product_id>/", views.BasketQuantityArrowDownAPIView.as_view(),
         name="api_arrow_down"),
]

from django.urls import path
from home import views


app_name = "home"

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path("about-us", views.AboutUsView.as_view(), name="about_us"),
    path("wish-list", views.WishListView.as_view(), name="wish_list"),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('wish-list-add/<int:product_id>/', views.WishListAddView.as_view(), name='wish_list_add'),
    path("advanced-search", views.AdvancedSearchView.as_view(), name="advanced_search"),
]

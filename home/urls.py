from django.urls import path
from home import views


app_name = "home"

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
]

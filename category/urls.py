from django.urls import path
from category import views

app_name = "category"

urlpatterns = [
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('producer-category/<int:producer_id>/<int:category_id>/', views.CategoryProducerView.as_view(),
         name='producer_category'),
]

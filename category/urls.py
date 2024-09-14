from django.urls import path
from home import views


app_name = "category"

urlpatterns = [
    path("categories", views.CategoryListView.as_view(), name="category"),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
]

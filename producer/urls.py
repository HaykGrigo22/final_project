from django.urls import path
from producer import views


app_name = "producer"

urlpatterns = [
    path("producers", views.ProducerList.as_view(), name="producers"),
    path("producer/<int:pk>/", views.ProducerDetailView.as_view(), name='producer_detail'),
    path("add_producer/", views.ProducerCreateView.as_view(), name='add_producer'),
]

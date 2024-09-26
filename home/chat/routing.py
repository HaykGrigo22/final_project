from django.urls import path
from home.chat import consumers


websocket_urlpatterns = [
    path("ws/", consumers.UserConsumer.as_asgi()),
]

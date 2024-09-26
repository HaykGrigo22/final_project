from django.urls import path
from chat import views

app_name = 'chat'

urlpatterns = [
    path('chat/<slug:slug>/', views.chat_room, name='course_chat_room'),
]

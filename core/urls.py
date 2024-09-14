from django.urls import path
from core import views

app_name = "user"
urlpatterns = [
    path("", views.AllUserView.as_view(), name="all_users"),
    path("send-email/", views.EmailView.as_view(), name="send_mail"),
    path("register/", views.RegisterForm.as_view(), name="register"),
    path("validate/<int:pk>/<tokenid>/", views.UserAccountActivation.as_view())
]

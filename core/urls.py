from django.urls import path
from core import views

app_name = "users"
urlpatterns = [
    path("send-email/", views.EmailView.as_view(), name="send_mail"),
    path("register/", views.RegisterForm.as_view(), name="register"),
    path("login/", views.LoginUser.as_view(), name="login"),
    path("logout/", views.LogoutUser.as_view(), name="logout"),
    path("validate/<int:pk>/<tokenid>/", views.UserAccountActivation.as_view())
]

from django.urls import path
from core import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from core.views import CustomTokenObtainPairView

app_name = "users"
urlpatterns = [
    path("send-email/", views.EmailView.as_view(), name="send_mail"),
    path("register/", views.RegisterForm.as_view(), name="register"),
    path("login/", views.LoginUser.as_view(), name="login"),
    path("logout/", views.LogoutUser.as_view(), name="logout"),
    path("validate/<int:pk>/<tokenid>/", views.UserAccountActivation.as_view()),

    path('api/token/', CustomTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),
]

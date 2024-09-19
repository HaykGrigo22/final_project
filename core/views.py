from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, FormView, CreateView
from django.contrib.auth import get_user_model
from django.conf import settings
from core.forms import EmailForm, UserRegisterForm
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.http import HttpResponse

from core.generate_token import generate_user_token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Custom validation using email instead of username
        username_field = 'email'  # Update this if your user model uses a different field
        username_value = attrs.get(username_field)
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'),
                            **{username_field: username_value, 'password': password})

        if not user:
            raise serializers.ValidationError(
                _('No active account found with the given credentials'),
                code='authorization',
            )

        return super().validate(attrs)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


User = get_user_model()


class EmailView(FormView):
    form_class = EmailForm
    template_name = "users/send_data_to_mail.html"

    def form_valid(self, form):
        to_email = form.cleaned_data.get("to_email")
        subject = form.cleaned_data.get("subject")
        content = form.cleaned_data.get("content")
        send_mail(subject=subject, from_email=settings.EMAIL_HOST,
                  message=content, recipient_list=[to_email],
                  fail_silently=False)
        return HttpResponseRedirect("/")


class RegisterForm(CreateView):
    template_name = "users/register.html"
    model = User
    form_class = UserRegisterForm
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        to_email = form.cleaned_data["email"]
        subject = "Account Registration"
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        token = generate_user_token.make_token(user)
        body = render_to_string("users/email_body.html",
                                {"domain": get_current_site(self.request),
                                 "user": user,
                                 "token": token,
                                 })
        email_instance = EmailMessage(subject=subject, body=body, to=[to_email])
        email_instance.send()
        return response


class UserAccountActivation(TemplateView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        token_id = kwargs.get("tokenid")
        user = User.objects.get(pk=pk)
        if generate_user_token.check_token(user, token_id):
            user.is_active = True
            user.save()
            return redirect("home:home")
        return HttpResponse("Invalid token")


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "users/login.html"
    success_url = "/"


class LogoutUser(LogoutView):
    next_page = '/'

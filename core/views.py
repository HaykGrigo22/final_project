import datetime

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView, DetailView, UpdateView
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.response import Response

from core.forms import EmailForm, UserRegisterForm, UserProfileForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import redirect
from django.http import HttpResponse

from core.generate_token import generate_user_token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _
from core.tasks import send_email_with_celery
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime, timedelta
from django.conf import settings


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username_field = 'email'
        username_value = attrs.get(username_field)
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'),
                            **{username_field: username_value, 'password': password})

        if not user:
            raise serializers.ValidationError(
                _('No active account found with the given credentials'),
                code='authorization',
            )

        data = super().validate(attrs)

        data.update({
            'user': user.email
        })

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        data = response.data
        access_token = data.get('access')
        refresh_token = data.get('refresh')

        access_token_expiration = datetime.now() + timedelta(
            minutes=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].seconds // 60)

        response.set_cookie(
            key='access_token',
            value=access_token,
            expires=access_token_expiration,
            httponly=True,
            secure=False,
            samesite='Lax',
        )

        refresh_token_expiration = datetime.now() + timedelta(
            days=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].days)
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            expires=refresh_token_expiration,
            httponly=True,
            secure=False,
            samesite='Lax',
        )

        return response


User = get_user_model()


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
                                {"domain": "http://127.0.0.1:8000",
                                 "user": user,
                                 "token": token,
                                 "site_name": "Hardware Magazine"
                                 })

        send_email_with_celery.delay(subject, body, [to_email])

        return response


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


class EmailViewCelery(FormView):
    form_class = EmailForm
    template_name = "users/send_data_to_mail.html"

    def form_valid(self, form):
        to_email = form.cleaned_data.get("to_email")
        subject = form.cleaned_data.get("subject")
        content = form.cleaned_data.get("content")

        send_email_with_celery.apply_async(kwargs={
            "subject": subject,
            "message": content,
            "recipient_list": [to_email],
        })
        return HttpResponseRedirect("/")


class UserAccountActivation(TemplateView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        token_id = kwargs.get("tokenid")
        user = User.objects.get(pk=pk)
        if generate_user_token.check_token(user, token_id):
            user.is_active = True
            user.save()
            # messages.success(request, "You entered successfully!!!")
            return redirect("home:home")
        return HttpResponse("Invalid token")


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=255)

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class LoginUser(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "users/login.html"
    success_url = "/"


class LogoutUser(LoginRequiredMixin, LogoutView):
    next_page = '/'


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user

        return context


class UpdateUserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/update_profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return User.objects.get(email=self.request.user)

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

User = get_user_model()


class AllUserView(TemplateView):
    template_name = "users/all_user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all()
        return context


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
        body = render_to_string("email_body.html",
                                {"domain": get_current_site(self.request),
                                 "user": user,
                                 "token": token,
                                 })
        email_instance = EmailMessage(subject=subject, body=body, to=[to_email])
        email_instance.send()
        print(user.is_active)
        return response


class UserAccountActivation(TemplateView):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        token_id = kwargs.get("tokenid")
        user = User.objects.get(pk=pk)
        if generate_user_token.check_token(user, token_id):
            user.is_active = True
            user.save()
            return redirect("user:all_users")
        return HttpResponse("Invalid token")

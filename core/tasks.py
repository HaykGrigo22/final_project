from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, EmailMessage

from main import settings

User = get_user_model()


@shared_task
def send_email_with_celery(subject, message, recipient_list):
    email_instance = EmailMessage(subject=subject, body=message, to=recipient_list, from_email=settings.EMAIL_HOST_USER)
    email_instance.send()

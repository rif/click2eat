from celery.decorators import task
from django.core.mail import send_mail

@task
def send_email_task(subject, body, send_from, send_to):
    send_mail(subject, body, send_from, send_to, fail_silently=False)

from celery.task import task
from django.core.mail import send_mail

@task
def send_email_task(subject, body, send_from, send_to):
    """
    sends mail using celery task scheduler
    """
    sent_to = [dest for dest in send_to]
    send_to.append('office@click2eat.ro')
    send_mail(subject, body, send_from, send_to, fail_silently=False)

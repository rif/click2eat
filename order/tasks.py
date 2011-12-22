from celery.task import task
from django.core.mail import send_mail

@task
def send_email_task(subject, body, send_from, send_to):
    """
    sends mail using celery task scheduler
    """
    sentto = [dest for dest in send_to]
    sentto.append('office@click2eat.ro')
    send_mail(subject, body, send_from, sentto, fail_silently=False)

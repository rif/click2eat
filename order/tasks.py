from celery.decorators import task
from django.core.mail import send_mail
#from celery.registry import tasks
#tasks.register(send_order_mail_to_restaurant)

@task
def send_order_mail_to_restaurant(subject, body, send_from, send_to):
    send_mail(subject, body, send_from, send_to, fail_silently=False)

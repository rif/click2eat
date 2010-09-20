from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    STATUS_CHOICES = (
      ('ST', 'Sent'),
      ('RV', 'Received'),
      ('DL', 'Delivered'),
      ('SV', 'Served'),
    )
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, editable=False)
    total_amount = models.FloatField()
    unit = models.ForeignKey('restaurant.Unit')

class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    item = models.ForeignKey('menu.Item')
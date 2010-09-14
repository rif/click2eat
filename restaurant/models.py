from django.db import models
from django.contrib.auth.models import User

class DeliveryArea(models.Model):
    name = models.CharField(max_length=200)

class Communication(models.Model):
    name = models.CharField(max_length=200)

class PartnerPackage(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField()

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    details = models.TextField()

class Rating(models.Model):
    user = models.OneToOneField(User)
    restaurant = models.ForeignKey(Unit)
    quality = models.SmallIntegerField()
    delivery_time = models.SmallIntegerField()
    feedback = models.TextField()

class DeliveryType(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()

class Employee(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    start_date = models.DateField()
    end_date = models.DateField()

class Unit(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    unit_devlivery = models.ForeignKey(DeliveryArea)
    overall_discount = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    delivery_time = models.IntegerField()
    communication = models.ForeignKey(Communication)
    package = models.ForeignKey(PartnerPackage)
    open_hours = models.CharField(max_length=10)
    minimum_ord_val = models.IntegerField()
    payment_method = models.ForeignKey(PaymentMethod)
    employee = models.ForeignKey(Employee)
    contact_person = models.CharField(max_length=50)
    rating = models.ForeignKey(Rating)
    logo_path = models.FilePathField()
    delivery_time_user = models.FloatField()
    delivery_type = models.ForeignKey(DeliveryType)
    info = models.TextField()
    active = models.BooleanField(default=True)

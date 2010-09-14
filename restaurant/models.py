from django.db import models

class Unit(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    unit_devlivery = models.ForeignKey(DeliveryArea)
    overall_discount = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    delicery_time = models.IntegerField()
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

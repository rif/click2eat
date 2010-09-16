from django.db import models

class VAT(models.Model):
  value = models.FloatField()

class ItemGroup(models.Model):
  internal_name = models.CharField(max_length=50)
  unit = models.ForeignKey('restaurant.Unit')
  exclusive = models.BooleanField()

class SubCategory(models.Model):
  name = models.CharField(max_length=50)

class Item(models.Model):
  unit = models.ForeignKey('restaurant.Unit')
  name = models.CharField(max_length=100)
  description = models.TextField()
  price = models.FloatField()
  vat = models.ForeignKey('VAT')
  discount = models.IntegerField()
  discount_time_start = models.DateTimeField()
  discount_time_end = models.DateTimeField()
  item_group = models.ForeignKey('ItemGroup')
  new_item_end_date = models.DateField()
  sub_category = models.ForeignKey('SubCategory')
  special = models.BooleanField()

class SpecialItem(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField()
  price = models.FloatField()
  vat = models.ForeignKey('VAT')
  time_start = models.DateTimeField()
  time_end = models.DateTimeField()
  item_group = models.ForeignKey('ItemGroup')
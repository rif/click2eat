from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class DeliveryAddress(models.Model):
  primary = models.BooleanField()
  city = models.CharField(max_length=50)
  street = models.CharField(max_length=50)
  house_number = models.CharField(max_length=5)
  street_number = models.CharField(max_length=5,null=True,blank=True)
  floor = models.SmallIntegerField()
  ap_number = models.SmallIntegerField()
  additional_info = models.TextField(null=True, blank=True)

class UserProfile(models.Model):
  GENDER_CHOICES = (
      ('M', 'Male'),
      ('F', 'Female'),
  )
  user = models.ForeignKey(User, unique=True)
  phone = models.CharField(max_length=15)
  newsletter = models.BooleanField(help_text="Do you want to receive our newsletter?")
  sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
  birth_date = models.DateField()
  delivery_address = models.ForeignKey('DeliveryAddress')

  def is_filled(self):
      return self.phone != '' or self.sex != '' or self.birthday != ''

  @models.permalink
  def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    
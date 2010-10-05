from django.test import TestCase
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from restaurant.models import Unit, Schedule, Interval

class UnitTest(TestCase):
    fixtures = ['restaurant.json']

    def setUp(self):
        self.user = User.objects.create_user('rif', 'test@test.te', 'test')
        self.unit = Unit.objects.get(pk=1)
    
    def test_schedule(self):
        s = Schedule(unit=self.unit)
        i1 = Interval(schedule=s, weekdays="1,2", start_hour="10:00", end_hour="12:00")
        self.assertTrue(i1._is_open(datetime(2010,10,5,11,0)))
        self.assertFalse(i1._is_open(datetime(2010,10,5,12,1)))
        self.assertFalse(i1._is_open(datetime(2010,10,5,9,0)))
        self.assertFalse(i1._is_open(datetime(2010,10,6,11,0)))

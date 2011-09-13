from django.test import TestCase
from datetime import datetime, time
from django.contrib.auth.models import User
from restaurant.models import Unit, Schedule, Interval

class UnitTest(TestCase):
    fixtures = ['restaurant.json']

    def setUp(self):
        self.user = User.objects.create_user('rif', 'test@test.te', 'test')
        self.unit = Unit.objects.get(pk=1)

    def test_schedule(self):
        s = Schedule(unit=self.unit)
        i1 = Interval(schedule=s, weekdays="1,2", start_hour=time(10,0), end_hour=time(12,0))
        self.assertTrue(i1._is_open(datetime(2010,10,5,11,0)))
        self.assertFalse(i1._is_open(datetime(2010,10,5,12,1)))
        self.assertFalse(i1._is_open(datetime(2010,10,5,9,0)))
        self.assertFalse(i1._is_open(datetime(2010,10,6,11,0)))

    def test_after_midnight_schedule(self):
        s = Schedule(unit=self.unit)
        i1 = Interval(schedule=s, weekdays="1,2,3,4,5,6,7", start_hour=time(10,0), end_hour=time(1,0))
        self.assertTrue(i1._is_open(datetime(2010,10,5,11,0)))
        self.assertTrue(i1._is_open(datetime(2010,10,5,23,15)))
        self.assertFalse(i1._is_open(datetime(2010,10,5,3,1)))

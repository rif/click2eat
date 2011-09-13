from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from restaurant.models import Unit
from menu.models import Promotion

class PromotionTest(TestCase):
    fixtures = ['restaurant.json', 'menu.json', 'order.json']
    def setUp(self):
        self.user = User.objects.create_user('rif', 'test@test.te', 'test')
        self.unit = Unit.objects.get(pk=1)

    def test_is_active_dates(self):
        p = Promotion(unit=self.unit, name="test", start_date=datetime(2010,10,2), end_date=datetime(2010,10,5))
        self.assertTrue(p._is_active(datetime(2010,10,3)))
        self.assertFalse(p._is_active(datetime(2010,10,1)))
        self.assertFalse(p._is_active(datetime(2010,10,6)))

    def test_is_active_weekday(self):
        p = Promotion(unit=self.unit, name="test", weekdays='1,2')
        self.assertTrue(p._is_active(datetime(2010,10,4)))
        self.assertTrue(p._is_active(datetime(2010,10,5)))
        self.assertFalse(p._is_active(datetime(2010,10,6)))

    def test_is_active_hours(self):
        p = Promotion(unit=self.unit, name="test", start_hour='10:00', end_hour='12:00')
        self.assertTrue(p._is_active(datetime(2010,10,4,11,0)))
        self.assertFalse(p._is_active(datetime(2010,10,4,9,59)))
        self.assertFalse(p._is_active(datetime(2010,10,4,12,1)))

    def test_is_active_dates_weekdays(self):
        p = Promotion(unit=self.unit, name="test", weekdays="1,2", start_date=datetime(2010,10,2), end_date=datetime(2010,10,5))
        self.assertTrue(p._is_active(datetime(2010,10,4)))
        self.assertFalse(p._is_active(datetime(2010,10,3)))
        self.assertFalse(p._is_active(datetime(2010,10,1)))
        self.assertFalse(p._is_active(datetime(2010,10,11)))

    def test_is_active_dates_hours(self):
        p = Promotion(unit=self.unit, name="test", start_date=datetime(2010,10,2), end_date=datetime(2010,10,5), start_hour='11:30', end_hour='12:15')
        self.assertTrue(p._is_active(datetime(2010,10,4,11,45)))
        self.assertFalse(p._is_active(datetime(2010,10,4,10,0)))
        self.assertFalse(p._is_active(datetime(2010,10,4,12,30)))
        self.assertFalse(p._is_active(datetime(2010,10,1,11,45)))


    def test_is_active_dates_weekdays_hours(self):
        p = Promotion(unit=self.unit, name="test", weekdays="1,2", start_date=datetime(2010,10,2), end_date=datetime(2010,10,5), start_hour='11:30', end_hour='12:15')
        self.assertTrue(p._is_active(datetime(2010,10,4,11,45)))
        self.assertFalse(p._is_active(datetime(2010,10,4,10,0)))
        self.assertFalse(p._is_active(datetime(2010,10,4,12,30)))
        self.assertFalse(p._is_active(datetime(2010,10,3,11,45)))
        self.assertFalse(p._is_active(datetime(2010,10,1,11,45)))
        self.assertFalse(p._is_active(datetime(2010,10,11,11,45)))

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Sum
from bonus.models import BonusTransaction
from userprofiles.models import UserProfile

class SimpleTest(TestCase):
    fixtures = ['users.json', 'userprofiles.json', 'bonus.json']

    def test_total_sum(self):
        user = User.objects.get(pk=2)
        self.assertEqual(6.0, user.get_profile().get_current_bonus())

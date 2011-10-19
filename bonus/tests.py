from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Sum
from bonus.models import Bonus

class SimpleTest(TestCase):
    fixtures = ['bonus.json', 'users.json', 'userprofiles.json']

    def test_total_sum(self):
        user = User.objects.get(pk=2)
        bonuses = Bonus.objects.filter(user__id = 2).filter(used=False)
        total = bonuses.aggregate(Sum('money'))
        self.assertEqual(user.get_profile().get_bonus_money(), round(total['money__sum'],2))

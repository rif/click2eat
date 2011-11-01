from django.test import TestCase
from django.contrib.auth.models import User

class SimpleTest(TestCase):
    fixtures = ['users.json', 'userprofiles.json', 'bonus.json', 'order.json']

    def test_total_sum(self):
        user = User.objects.get(pk=2)
        self.assertEqual(6.0, user.get_profile().get_current_bonus())

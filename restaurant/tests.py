from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from restaurant.models import Unit

class UnitTest(TestCase):
    fixtures = ['restaurant.json']

    def setUp(self):
        self.user = User.objects.create_user('rif', 'test@test.te', 'test')
        
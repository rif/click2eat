from django.test import TestCase
from django.core.urlresolvers import reverse

class MobileTest(TestCase):
    def test_cart_total(self):
        r = self.client.get(self.client.get(reverse('mobile:shop', args=[1])))
        self.assertEquals('10', r.content)


from django.test import TestCase
from django.core.urlresolvers import reverse
from restaurant.models import Unit
from order.shopping_service import OrderCarts

class MobileTest(TestCase):
    fixtures = ['restaurant.json', 'menu.json', 'users.json']

    def test_cart_total(self):
        login_successful = self.client.login(username='rif', password='test')
        self.assertTrue(login_successful)
        r = self.client.get(reverse('order:shop', args=[1, "rif", '1-0']))
        self.assertEqual(200, r.status_code)
        self.assertTrue('<span id="order-total">12.0</span>' in r.content)

    def test_session_item(self):
        self.client.login(username='rif', password='test')
        r = self.client.get(reverse('order:shop', args=[1, "rif", '1-0']))
        self.assertEqual(200, r.status_code)
        oc = OrderCarts(self.client.session, '1')
        self.assertEqual(12, oc.get_total_sum())

    def test_session_motd(self):
        self.client.login(username='rif', password='test')
        r = self.client.get(reverse('order:shop', args=[1, "rif", 'm1-0']))
        self.assertEqual(200, r.status_code)
        oc = OrderCarts(self.client.session, '1')
        self.assertEqual(10, oc.get_total_sum())

    def test_session_top(self):
        self.client.login(username='rif', password='test')
        self.client.get(reverse('order:shop', args=[1, "rif", '1-0']))
        r = self.client.get(reverse('order:shop', args=["1", "rif", '1-0_1']))
        self.assertEqual(200, r.status_code)
        oc = OrderCarts(self.client.session, '1')
        self.assertEqual(13, oc.get_total_sum())

    def test_session_first_top(self):
        self.client.login(username='rif', password='test')
        r = self.client.get(reverse('order:shop', args=[1, "rif", '1-0_1']))
        self.assertEqual(200, r.status_code)
        self.assertTrue('<span id="order-total"></span>' in r.content)

    def test_session_top_without_item(self):
        self.client.login(username='rif', password='test')
        r = self.client.get(reverse('order:shop', args=[1, "rif", '2-0']))
        r = self.client.get(reverse('order:shop', args=[1, "rif", '1-0_1']))
        self.assertEqual(200, r.status_code)
        self.assertTrue('<span id="order-total">11.99</span>' in r.content)

    def test_min_order(self):
        u = Unit.objects.get(id=1)
        u.minimum_ord_val = 100
        u.save()
        self.client.login(username='rif', password='test')
        self.client.get(reverse('order:shop', args=[1, "rif", '1-0']))
        r = self.client.get(reverse('mobile:send-order', args=['1']))
        self.assertEqual(200, r.status_code)
        self.assertTrue(r.content in ['{"error": "2e65"}','{"error": "2e61"}']) # maybe closed

    def test_decr_clean_top(self):
        u = Unit.objects.get(id=1)
        u.minimum_ord_val = 100
        u.save()
        self.client.login(username='rif', password='test')
        self.client.get(reverse('order:shop', args=[1, "rif", '1-0']))
        r = self.client.get(reverse('order:shop', args=[1, "rif", '1-0_1']))
        self.assertEqual(200, r.status_code)
        oc = OrderCarts(self.client.session, '1')
        self.assertEqual(13, oc.get_total_sum())

    def test_decr(self):
        u = Unit.objects.get(id=1)
        u.minimum_ord_val = 100
        u.save()
        self.client.login(username='rif', password='test')
        oc = OrderCarts(self.client.session, '1')
        self.client.get(reverse('order:shop', args=[1, "rif", '1-0']))
        r = self.client.get(reverse('order:decr-item', args=[1, "rif", '1-0']))
        self.assertEqual(200, r.status_code)
        self.assertEqual(0, oc.get_total_sum())

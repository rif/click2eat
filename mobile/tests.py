from django.test import TestCase
from django.core.urlresolvers import reverse
from restaurant.models import Unit

class MobileTest(TestCase):
    fixtures = ['restaurant.json', 'menu.json', 'users.json']

    def test_cart_total(self):
        login_successful = self.client.login(username='rif', password='test')
        self.assertTrue(login_successful)
        r = self.client.get(reverse('order:shop', args=['rif', '1']))
        self.assertEqual(200, r.status_code)
        self.assertEquals('{"price": 10.0, "total": 10.0, "subtotal": 10.0, "id": "1", "name": "Tocanita de puioc"}', r.content)

    def test_session_item(self):
        self.client.login(username='rif', password='test')
        r = self.client.get(reverse('order:shop', args=['rif', '1']))
        self.assertEqual(200, r.status_code)
        self.assertEquals( {u'1': [1, 10.0, u'Tocanita de puioc']}, self.client.session['1:rif'])

    def test_session_motd(self):
        self.client.login(username='rif', password='test')
        r = self.client.get(reverse('order:shop', args=['rif', 'm1']))
        self.assertEqual(200, r.status_code)
        self.assertEquals({u'm1': [1, 10.0, u'Meniu complet cu 10 lei']}, self.client.session['1:rif'])

    def test_session_top(self):
        self.client.login(username='rif', password='test')
        self.client.get(reverse('order:shop', args=['rif', '1']))
        r = self.client.get(reverse('order:shop', args=['rif', '1_1']))
        self.assertEqual(200, r.status_code)
        self.assertEquals({u'1': [1, 10.0, u'Tocanita de puioc'], u'1_1': [1, 1.0, u'Cascaval']}, self.client.session['1:rif'])

    def test_session_first_top(self):
        self.client.login(username='rif', password='test')
        r = self.client.get(reverse('order:shop', args=['rif', '1_1']))
        self.assertEqual(200, r.status_code)
        self.assertEquals('{"error": "2e62"}', r.content)

    def test_session_top_without_item(self):
        self.client.login(username='rif', password='test')
        r = self.client.get(reverse('order:shop', args=['rif', '2']))
        r = self.client.get(reverse('order:shop', args=['rif', '1_1']))
        self.assertEqual(200, r.status_code)
        self.assertEquals('{"error": "2e6z"}', r.content)

    def test_min_order(self):
        u = Unit.objects.get(id=1)
        u.minimum_ord_val = 100
        u.save()
        self.client.login(username='rif', password='test')
        self.client.get(reverse('order:shop', args=['rif', '1']))
        r = self.client.get(reverse('order:send-order', args=['1']))
        self.assertEqual(200, r.status_code)
        self.assertTrue(r.content in ['{"error": "2e65"}','{"error": "2e61"}']) # maybe closed

    def test_decr_clean_top(self):
        u = Unit.objects.get(id=1)
        u.minimum_ord_val = 100
        u.save()
        self.client.login(username='rif', password='test')
        self.client.get(reverse('order:shop', args=['rif', '1']))
        self.client.get(reverse('order:shop', args=['rif', '1_1']))
        r = self.client.get(reverse('order:decr-item', args=['rif', '1', '1']))
        self.assertEqual(200, r.status_code)
        self.assertTrue('1:rif' not in self.client.session)

    def test_incr_decr(self):
        u = Unit.objects.get(id=1)
        u.minimum_ord_val = 100
        u.save()
        self.client.login(username='rif', password='test')
        self.client.get(reverse('order:shop', args=['rif', '1']))
        r = self.client.get(reverse('order:incr-item', args=['rif', '1', '1']))
        self.assertEquals({u'1': [2, 10.0, u'Tocanita de puioc']}, self.client.session['1:rif'])
        r = self.client.get(reverse('order:decr-item', args=['rif', '1', '1']))
        self.assertEqual(200, r.status_code)
        self.assertEquals({u'1': [1, 10.0, u'Tocanita de puioc']}, self.client.session['1:rif'])

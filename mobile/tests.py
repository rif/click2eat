from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class MobileTest(TestCase):
    fixtures = ['restaurant.json', 'menu.json', 'users.json']    
    
    def test_cart_total(self):
        login_successful = self.client.login(username='rif', password='test')
        self.assertTrue(login_successful)
        r = self.client.get(reverse('mobile:shop', args=[1]))
        self.assertEqual(200, r.status_code)
        self.assertEquals('{"count": 10.0}', r.content)

    def test_session_item(self):
        self.client.login(username='rif', password='test')        
        r = self.client.get(reverse('mobile:shop', args=[1]))
        self.assertEqual(200, r.status_code)
        self.assertEquals( {u'1': [1, 10.0, u'Tocanita de puioc']}, self.client.session['1'])
        
    def test_session_motd(self):
        self.client.login(username='rif', password='test')        
        r = self.client.get(reverse('mobile:shop', args=['m1']))
        self.assertEqual(200, r.status_code)
        self.assertEquals({u'm1': [1, 10.0, u'Meniu complet cu 10 lei']}, self.client.session['1'])
    
    def test_session_top(self):
        self.client.login(username='rif', password='test')        
        r = self.client.get(reverse('mobile:shop', args=['1_1']))
        self.assertEqual(200, r.status_code)
        self.assertEquals({u'1_1': [1, 1.0, u'Cascaval']}, self.client.session['1'])

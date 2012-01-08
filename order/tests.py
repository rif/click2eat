from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime
from order.models import Order, OrderItem
from restaurant.models import Unit
from menu.models import Item
from time import time
from order.shopping_service import consume_bonus

def uid(id):
    return '%s!%s-0' %(int(time()*1000), id)

class OrderTest(TestCase):
  fixtures = ['restaurant.json', 'menu.json', 'order.json', 'users.json', 'userprofiles.json', 'bonus.json']
  def setUp(self):
    User.objects.create_user('rif0', 'rif@test.te', 'test')
    User.objects.create_user('rif1', 'rif1@test.te', 'test')
    self.user = User.objects.create_user('bobo1', 'bobo@test.te', 'test')    
    self.unit = Unit.objects.get(pk=1)
    self.unit.admin_users='rif0,bobo1'
    self.unit.save()

  def test_total_amount(self):
    ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
    OrderItem.objects.create(order=ord, old_price = 3, item=Item.objects.get(pk=1))
    OrderItem.objects.create(order=ord, old_price = 7, item=Item.objects.get(pk=2))
    self.assertEqual(10, ord.total_amount)

  def test_cart_subtotal(self):
    ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=1), old_price = 3, cart="1")
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=2), old_price = 4, cart="1")
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=2), old_price = 5, cart="2")
    self.assertEqual(12, ord.total_amount)
    self.assertEqual(7, ord.get_cart_subtotal("1"))
    self.assertEqual(5, ord.get_cart_subtotal("2"))

  def test_get_carts(self):
    ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
    oi1 = OrderItem.objects.create(order=ord, item=Item.objects.get(pk=1), cart="1")
    oi2 = OrderItem.objects.create(order=ord, item=Item.objects.get(pk=2), cart="1")
    oi3 = OrderItem.objects.create(order=ord, item=Item.objects.get(pk=3), cart="2")
    self.assertEqual(oi1, ord.get_carts()['1'][0])
    self.assertEqual(oi2, ord.get_carts()['1'][1])
    self.assertEqual(oi3, ord.get_carts()['2'][0])

  def test_clone(self):
    ord1 = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
    OrderItem.objects.create(order=ord1, item=Item.objects.get(pk=1), cart="1")
    OrderItem.objects.create(order=ord1, item=Item.objects.get(pk=2), cart="1")
    OrderItem.objects.create(order=ord1, item=Item.objects.get(pk=3), cart="2")
    ord2 = ord1.clone()
    delta = datetime.now() - ord2.creation_date
    self.assertTrue(delta.seconds < 5)
    self.assertEqual(ord1.employee, ord2.employee)
    self.assertEqual('ST', ord2.status)
    self.assertEqual(3, ord2.orderitem_set.count())
    self.assertEqual(21.99, ord2.total_amount)

  def test_mark_delivered_weird(self):
      ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
      self.client.login(username='rif0', password='test')
      r = self.client.get(reverse('order:restaurant_detail', args=[ord.id]))
      self.assertEqual(200, r.status_code)

  def test_mark_delivered(self):
      self.assertTrue('bobo' in self.unit.admin_users)
      ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
      self.client.login(username='bobo1', password='test')
      r = self.client.get(reverse('order:restaurant_deliver', args=[ord.id]))
      self.assertEqual(200, r.status_code)
      self.assertEqual('Livrata', r.content)

  def test_restricted_views(self):
      ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
      self.client.login(username='bobo1', password='test')
      r = self.client.get(reverse('order:restaurant_detail', args=[ord.id]))
      self.assertEqual(200, r.status_code)
      r = self.client.get(reverse('order:restaurant_list', args=[self.unit.id]))
      self.assertEqual(200, r.status_code)
      r = self.client.get(reverse('order:restaurant_list_ajax', args=[self.unit.id]))
      self.assertEqual(200, r.status_code)
      self.client.login(username='rif1', password='test')
      r = self.client.get(reverse('order:restaurant_detail', args=[ord.id]))
      self.assertEqual(403, r.status_code)
      r = self.client.get(reverse('order:restaurant_list', args=[self.unit.id]))
      self.assertEqual(403, r.status_code)
      r = self.client.get(reverse('order:restaurant_list_ajax', args=[self.unit.id]))
      self.assertEqual(403, r.status_code)
      r = self.client.get(reverse('order:restaurant_deliver', args=[ord.id]))
      self.assertEqual(403, r.status_code)

  def test_count_amount(self):
    ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
    OrderItem.objects.create(order=ord, old_price = 5, item=Item.objects.get(pk=1))
    OrderItem.objects.create(order=ord, count=5, old_price = 5, item=Item.objects.get(pk=2))
    self.assertEqual(30, ord.total_amount)

  def test_count_add(self):
     self.client.login(username='rif0', password='test')
     r = self.client.get(reverse('order:shop', args=[self.unit.id, "rif0", uid('1')]))
     self.assertEqual(200, r.status_code)
     self.assertTrue("Tocanita de puioc" in r.content)

  def test_count_remove(self):
    self.client.login(username='rif0', password='test')
    self.client.get(reverse('order:shop', args=[self.unit.id, "rif0", uid('1')]))
    r = self.client.get(reverse('order:decr-item', args=[self.unit.id, "rif0", uid('1')]))
    self.assertEqual(200, r.status_code)
    self.assertTrue('<span id="order-total">12.0</span>' in r.content)

  def test_subtotal_cart(self):
     self.client.login(username='rif0', password='test')
     self.client.get(reverse('order:shop', args=[self.unit.id, "rif0", uid('1')]))
     self.client.get(reverse('order:shop', args=[self.unit.id, "rif0", uid('2')]))
     self.client.get(reverse('order:shop', args=[self.unit.id, "rif0", uid('3')]))
     r = self.client.get(reverse('order:shopping-cart', args=[1]))
     self.assertEqual(200, r.status_code)
     self.assertTrue('<span class="cart-subtotal">23.99</span>' in r.content)

  def test_total_cart(self):
     self.client.login(username='rif0', password='test')
     self.client.get(reverse('order:shop', args=[self.unit.id, "rif0", uid('1')]))
     self.client.get(reverse('order:shop', args=[self.unit.id, "rif0", uid('2')]))
     self.client.get(reverse('order:shop', args=[self.unit.id, "rif0", uid('2')]))
     self.client.get(reverse('order:shop', args=[self.unit.id, "mama", uid('1')]))
     self.client.get(reverse('order:shop', args=[self.unit.id, "mama", uid('1')]))
     r = self.client.get(reverse('order:shopping-cart', args=[1]))
     self.assertEqual(200, r.status_code)
     self.assertTrue('<span class="cart-subtotal">33.98</span>' in r.content)
     self.assertTrue('<span class="cart-subtotal">24.0</span>' in r.content)
     self.assertTrue('<span id="order-total">57.98</span>' in r.content)

  def test_total(self):
     self.client.login(username='rif0', password='test')
     self.client.get(reverse('order:shop', args=[self.unit.id, "rif0", uid('1')]))
     self.client.get(reverse('order:shop', args=[self.unit.id, "rif0", uid('2')]))
     r = self.client.get(reverse('order:shop', args=[self.unit.id, "rif", uid('2')]))
     self.assertEqual(200, r.status_code)
     self.assertTrue('<span id="order-total">33.98</span>' in r.content)

  def test_no_exception_incr_decr(self):
     self.client.login(username='rif0', password='test')
     r = self.client.get(reverse('order:incr-item', args=[self.unit.id, "tata", uid('1')]))
     self.assertTrue('<span id="order-total">0.0</span>' in r.content)
     r = self.client.get(reverse('order:decr-item', args=[self.unit.id, "rif0", uid('1')]))
     self.assertTrue('<span id="order-total">0.0</span>' in r.content)
     self.client.get(reverse('order:shop', args=[self.unit.id, "rif0", uid('1')]))
     r = self.client.get(reverse('order:incr-item', args=[self.unit.id, "rif0", uid('1')]))
     self.assertTrue('<span id="order-total">12.0</span>' in r.content)
     r = self.client.get(reverse('order:decr-item', args=[self.unit.id, "rif0", uid('1')]))
     self.assertTrue('<span id="order-total">12.0</span>' in r.content)

  def test_not_enough_bonus_money(self):
      user = User.objects.get(id=2)      
      ord1 = Order.objects.create(user=user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
      OrderItem.objects.create(order=ord1, item=Item.objects.get(pk=1), cart="1")
      result = consume_bonus(ord1)
      self.assertEqual(0, result)
      self.assertEqual(6.0, user.get_profile().get_current_bonus())
      #self.assertFalse(ord1.paid_with_bonus)

  def test_use_partial_bonus_money(self):
      user = User.objects.get(id=2)
      ord1 = Order.objects.create(user=user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
      OrderItem.objects.create(order=ord1, item=Item.objects.get(pk=3), cart="1", )
      result = consume_bonus(ord1)
      self.assertEquals(0, result)      
      self.assertEqual(6.0, user.get_profile().get_current_bonus())
      self.assertTrue(ord1.paid_with_bonus)

  def test_use_total_bonus_money(self):        
      user = User.objects.get(id=2)            
      ord1 = Order.objects.create(user=user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
      oi = OrderItem.objects.create(order=ord1, item=Item.objects.get(pk=3), cart="1", )
      oi.old_price = 6.0
      oi.save()
      result = consume_bonus(ord1)
      self.assertEquals(0, result)
      self.assertEqual(0, user.get_profile().get_current_bonus())

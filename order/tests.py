from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime
from order.models import Order, OrderItem
from restaurant.models import Unit
from menu.models import Item

class OrderTest(TestCase):
  fixtures = ['restaurant.json', 'menu.json', 'order.json']
  def setUp(self):
    self.user = User.objects.create_user('rif', 'rif@test.te', 'test')
    self.user = User.objects.create_user('rif1', 'rif1@test.te', 'test')
    self.user = User.objects.create_user('bobo', 'bobo@test.te', 'test')
    self.unit = Unit.objects.get(pk=1)
    self.unit.admin_users='rif,bobo'
    self.unit.save()

  def test_abandoned_empty_removal(self):
    count = Order.objects.count()
    old = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
    old.creation_date = datetime(2010, 9, 24)
    old.save()
    self.assertEqual(count + 1, Order.objects.count())
    self.assertEqual(0.0, old.total_amount)
    old.delete_abandoned()
    self.assertEqual(count, Order.objects.count())

  def test_abandoned_nonempty_status(self):
    count = Order.objects.count()
    old = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
    old.creation_date = datetime(2010, 9, 24)
    old.save()
    self.assertEqual(count + 1, Order.objects.count())
    OrderItem.objects.create(order=old, item=Item.objects.get(pk=1))
    self.assertEqual(10.0, old.total_amount)
    old.delete_abandoned()
    self.assertEqual(count, Order.objects.count())

  def test_total_amount(self):
    ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=1))
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=2))
    self.assertEqual(20.99, ord.total_amount)

  def test_cart_subtotal(self):
    ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=1), cart="1")
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=2), cart="1")
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=2), cart="2")
    self.assertEqual(31.98, ord.total_amount)
    self.assertEqual(20.99, ord.get_cart_subtotal("1"))
    self.assertEqual(10.99, ord.get_cart_subtotal("2"))

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
    self.assertEqual('CR', ord2.status)
    self.assertEqual(3, ord2.orderitem_set.count())
    self.assertEqual(21.99, ord2.total_amount)

  def test_mark_delivered_weird(self):
      ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
      self.client.login(username='rif', password='test')
      r = self.client.get(reverse('order:restaurant_detail', args=[ord.id]))
      self.assertEqual(200, r.status_code)


  def test_mark_delivered(self):
      self.assertTrue('bobo' in self.unit.admin_users)
      ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
      self.client.login(username='bobo', password='test')
      r = self.client.get(reverse('order:restaurant_deliver', args=[ord.id]))
      self.assertEqual(200, r.status_code)
      self.assertEqual('Livrat', r.content)

  def test_restricted_views(self):
      ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
      self.client.login(username='bobo', password='test')
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
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=1))
    OrderItem.objects.create(order=ord, count=5, item=Item.objects.get(pk=2))
    self.assertEqual(64.95, ord.total_amount)

  def test_count_add(self):
     self.client.login(username='rif', password='test')
     r = self.client.get(reverse('order:shop', args=["rif", 1]))
     self.assertEqual(200, r.status_code)
     self.assertEqual('{"count": 10.0, "price": 10.0, "id": "1", "name": "Tocanita de puioc"}', r.content)

  def test_count_remove(self):
    self.client.login(username='rif', password='test')
    self.client.get(reverse('order:shop', args=["rif", 1]))
    r = self.client.get(reverse('order:decr-item', args=['rif', 1, 1]))
    self.assertEqual(200, r.status_code)
    self.assertEqual('{"count": 0.0}', r.content)

  def test_subtotal_cart(self):
     self.client.login(username='rif', password='test')
     self.client.get(reverse('order:shop', args=["rif", 1]))
     self.client.get(reverse('order:shop', args=["rif", 2]))
     self.client.get(reverse('order:shop', args=["rif", 2]))
     r = self.client.get(reverse('order:shopping-cart', args=[1]))
     self.assertEqual(200, r.status_code)
     self.assertTrue('<span class="cart-subtotal">31.98</span>' in r.content)

  def test_total_cart(self):
     self.client.login(username='rif', password='test')
     self.client.get(reverse('order:shop', args=["rif", 1]))
     self.client.get(reverse('order:shop', args=["rif", 2]))
     self.client.get(reverse('order:shop', args=["rif", 2]))
     self.client.get(reverse('order:shop', args=["mama", 1]))
     self.client.get(reverse('order:shop', args=["mama", 1]))
     r = self.client.get(reverse('order:shopping-cart', args=[1]))
     self.assertEqual(200, r.status_code)
     self.assertTrue('<span class="cart-subtotal">31.98</span>' in r.content)
     self.assertTrue('<span class="cart-subtotal">20.0</span>' in r.content)
     self.assertTrue('<span id="order-total">51.98</span>' in r.content)

  def test_total(self):
     self.client.login(username='rif', password='test')
     self.client.get(reverse('order:shop', args=["rif", 1]))
     self.client.get(reverse('order:shop', args=["rif", 2]))
     r = self.client.get(reverse('order:shop', args=["rif", 2]))
     self.assertEqual(200, r.status_code)
     self.assertEqual('{"count": 31.98, "price": 10.99, "id": "2", "name": "Supa de rosii"}', r.content)

  def test_no_exception_incr_decr(self):
     self.client.login(username='rif', password='test')
     r = self.client.get(reverse('order:incr-item', args=['tata', 1, 1]))
     self.assertEqual('{"error": "29a"}', r.content)
     r = self.client.get(reverse('order:decr-item', args=['rif', 1, 1]))
     self.assertEqual('{"error": "29a"}', r.content)
     self.client.get(reverse('order:shop', args=["rif", 1]))
     r = self.client.get(reverse('order:incr-item', args=['rif', 1, 2]))
     self.assertEqual('{"error": "29a"}', r.content)
     r = self.client.get(reverse('order:decr-item', args=['rif', 1, 2]))
     self.assertEqual('{"error": "29a"}', r.content)

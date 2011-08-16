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

  def test_abandoned_empty_removal(self):
    count = Order.objects.count()
    old = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
    old.creation_date = datetime(2010, 9, 24)
    old.save()
    self.assertEqual(count + 1, Order.objects.count())
    self.assertEqual(0.0, old.total_amount)
    old.is_abandoned()
    self.assertEqual(count, Order.objects.count())

  def test_abandoned_nonempty_status(self):
    count = Order.objects.count()
    old = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
    old.creation_date = datetime(2010, 9, 24)
    old.save()
    self.assertEqual(count + 1, Order.objects.count())
    OrderItem.objects.create(order=old, item=Item.objects.get(pk=1))
    self.assertEqual(9.0, old.total_amount)
    old.is_abandoned()
    self.assertEqual(count + 1, Order.objects.count())
    self.assertEqual('AB', old.status)

  def test_total_amount(self):
    ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=1))
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=2))
    self.assertEqual(19.0, ord.total_amount)

  def test_cart_subtotal(self):
    ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=1), cart="1")
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=2), cart="1")
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=2), cart="2")
    self.assertEqual(29.0, ord.total_amount)
    self.assertEqual(19.0, ord.get_cart_subtotal("1"))
    self.assertEqual(10, ord.get_cart_subtotal("2"))

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
    self.assertEqual(20.0, ord2.total_amount)
  
  def test_mark_delivered(self):
      ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
      self.client.login(username='rif', password='test')
      r = self.client.get(reverse('order:restaurant_detail', args=[ord.id]))
      self.assertEqual(200, r.status_code)
      #self.assertEqual(u'RV', ord.status)
  
  def test_mark_delivered(self):
      ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
      self.client.login(username='bobo', password='test')
      r = self.client.get(reverse('order:restaurant_deliver', args=[ord.id]))
      self.assertEqual(200, r.status_code)
      self.assertEqual('Livrat', r.content)
      #self.assertEqual(u'DL', ord.status)
  
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
    self.assertEqual(59.0, ord.total_amount)

  def test_count_add(self):
     ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
     oi = OrderItem.objects.create(order=ord, item=Item.objects.get(pk=1), cart="rif")
     self.assertEqual(1, oi.count)
     self.client.login(username='rif', password='test')
     r = self.client.get(reverse('order:add_item', args=[oi.id, "rif"]))
#     self.assertEqual(200, r.status_code)
#     self.assertEqual(2, oi.count)

  def test_count_remove(self):
    ord = Order.objects.create(user=self.user, unit_id=self.unit.id, employee_id=self.unit.employee_id)
    oi = OrderItem.objects.create(order=ord, count=2, item=Item.objects.get(pk=1), cart="rif")
    self.assertEqual(2, oi.count)
    self.client.login(username='rif', password='test')
    r = self.client.get(reverse('order:remove_item', args=[oi.id]))
    self.assertEqual(200, r.status_code)
    self.assertEqual("1", r.content)

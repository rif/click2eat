from django.test import TestCase
from django.contrib.auth.models import User
from datetime import datetime
from order.models import Order, OrderItem
from restaurant.models import Unit
from menu.models import Item

class OrderTest(TestCase):
  fixtures = ['restaurant.json', 'menu.json', 'order.json']
  def setUp(self):
    self.user = User.objects.create_user('rif', 'test@test.te', 'test')
    self.unit = Unit.objects.get(pk=1)

  def test_abandoned_empty_removal(self):
    old = Order.objects.create(user=self.user, unit=self.unit)
    old.creation_date=datetime(2010,9,24)
    old.save()
    self.failUnlessEqual(6, Order.objects.count())
    self.failUnlessEqual(0.0, old.total_amount)
    old.is_abandoned()
    self.failUnlessEqual(5, Order.objects.count())

  def test_abandoned_nonempty_status(self):
    old = Order.objects.create(user=self.user, unit=self.unit)
    old.creation_date=datetime(2010,9,24)
    old.save()
    self.failUnlessEqual(6, Order.objects.count())
    OrderItem.objects.create(order=old, item=Item.objects.get(pk=1))
    self.failUnlessEqual(1.23, old.total_amount)
    old.is_abandoned()
    self.failUnlessEqual(6, Order.objects.count())
    self.failUnlessEqual('AB', old.status)

  def test_total_amount(self):
    ord = Order.objects.create(user=self.user, unit=self.unit)
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=1))
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=2))
    self.failUnlessEqual(11.23, ord.total_amount)

  def test_cart_subtotal(self):
    ord = Order.objects.create(user=self.user, unit=self.unit)
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=1), cart="1")
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=2), cart="1")
    OrderItem.objects.create(order=ord, item=Item.objects.get(pk=2), cart="2")
    self.failUnlessEqual(21.23, ord.total_amount)
    self.failUnlessEqual(11.23, ord.get_cart_subtotal("1"))
    self.failUnlessEqual(10, ord.get_cart_subtotal("2"))


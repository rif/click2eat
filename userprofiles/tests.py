from django.test import TestCase
from django.contrib.auth.models import User
from userprofiles.models import DeliveryAddress

class DeliveryAddressTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('rif', 'test@test.te', 'test')
        self.da1 = DeliveryAddress.objects.create(user=self.user,primary=True,city='1',street='1',house_number='1',floor=1,ap_number=1)
        
    def test_primary_uniquenes(self):
        das = DeliveryAddress.objects.filter(user__id=self.user.id).filter(primary=True)
        self.failUnlessEqual(das.count(), 1)
        DeliveryAddress.objects.create(user=self.user,primary=True,city='1',street='1',house_number='1',floor=1,ap_number=1)
        all_count = DeliveryAddress.objects.count()
        self.failUnlessEqual(all_count, 2)
        das = DeliveryAddress.objects.filter(user__id=self.user.id).filter(primary=True)
        # still one primary address
        self.failUnlessEqual(das.count(), 1)

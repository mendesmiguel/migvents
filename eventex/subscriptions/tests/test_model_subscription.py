from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(name='Mancebo Legal',
                           cpf='12345678901',
                           email='mancebo@legal.com',
                           phone='21 2222-3333')
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Mancebo Legal', str(self.obj))

    def test_paid_default_false(self):
        self.assertEqual(False, self.obj.paid)

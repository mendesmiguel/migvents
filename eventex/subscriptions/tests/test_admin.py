from unittest.mock import Mock

from django.test import TestCase
from eventex.subscriptions.admin import Subscription, SubscriptionModelAdmin, admin


class SubscriptionModelAdminTest(TestCase):

    def setUp(self):
        Subscription.objects.create(name="Mancebo Legal", cpf='12345678901',
                                    email='mancebo@legal.me', phone='21 99876-5432')
        self.model_admin = SubscriptionModelAdmin(Subscription, admin.site)
        query_set = Subscription.objects.all()
        self.mock = Mock()
        self.old_message_user = SubscriptionModelAdmin.message_user
        SubscriptionModelAdmin.message_user = self.mock
        self.model_admin.mark_as_paid(None, query_set)

    def test_has_action(self):
        self.assertIn('mark_as_paid', self.model_admin.actions)

    def test_mark_all(self):
        self.assertEqual(1, Subscription.objects.filter(paid=True).count())

    def test_message_user(self):
        self.mock.assert_called_once_with(None, "1 incrição foi marcada como paga com sucesso.")

    def tearDown(self):
        SubscriptionModelAdmin.message_user = self.old_message_user

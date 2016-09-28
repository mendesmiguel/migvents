from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription
from django.shortcuts import resolve_url as r

NEW_SUBSCRIPTION = r('subscriptions:new')


class SubscribeGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(NEW_SUBSCRIPTION)

    def test_get(self):
        """Get /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Must contain form elements"""
        tags = (
            ('<form', 1),
            ('<input', 6),
            ('type="text"', 3),
            ('type="email"', 1),
            ('type="submit"', 1)
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """Must contain csrf token"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must be a instance of SubscriptionForm"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribeValidPost(TestCase):
    def setUp(self):
        data = dict(name="Mancebo Legal", cpf='12345678901',
                    email='mancebo@legal.me', phone='21 99876-5432')

        self.resp = self.client.post(NEW_SUBSCRIPTION, data)

    def test_post(self):
        """Valid POST redirect to /inscricao/1"""
        self.assertRedirects(self.resp, '/inscricao/1/')

    def test_send_subscribe_mail(self):
        """Must send email after post"""
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post(NEW_SUBSCRIPTION, {})

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_has_erros(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())


class TemplateRegressionTest(TestCase):

    def test_template_has_non_field_errors(self):
        invalid_data = dict(name='Mancebo Legal', cpf='12345678901')
        response = self.client.post(NEW_SUBSCRIPTION, invalid_data)

        self.assertContains(response, '<ul class="errorlist nonfield">')
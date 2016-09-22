from django.test import TestCase
from django.shortcuts import resolve_url as r

class HomeTest(TestCase):

    def setUp(self):
        """setUp get response"""
        self.response = self.client.get(r('home'))

    def test_get(self):
        """Test successful response code"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Test expected template used"""
        self.assertTemplateUsed(self.response, 'index.html')

    def test_subscription_link(self):
        expected = 'href="{}"'.format(r('subscriptions:new'))
        self.assertContains(self.response, expected)

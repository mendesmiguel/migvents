from django.test import TestCase


class HomeTest(TestCase):

    def setUp(self):
        """setUp get response"""
        self.response = self.client.get('/')

    def test_get(self):
        """Test successful response code"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Test expected template used"""
        self.assertTemplateUsed(self.response, 'index.html')

    def test_subscription_link(self):
        self.assertContains(self.response, 'href="/inscricao/"')

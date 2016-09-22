from django.core import mail
from django.test import TestCase


class SubscribeValidPost(TestCase):
    def setUp(self):
        data = dict(name="Mancebo Legal", cpf='12345678901',
                    email='mancebo@legal.me', phone='21 99876-5432')

        self.resp = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_mail_subject(self):
        expect = 'Confirmação de Inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_mail_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_mail_to(self):
        expect = ['contato@eventex.com.br', 'mancebo@legal.me']
        self.assertEqual(expect, self.email.to)

    def test_subscription_mail_body(self):
        contents = [
            'Mancebo Legal',
            'mancebo@legal.me',
            '12345678901',
            '21 99876-5432'
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)

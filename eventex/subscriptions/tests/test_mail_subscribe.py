from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Lieverton Horn', cpf='12345678901',
                    email='lievertonh@gmail.com', phone='42-3252-1698')
        self.response = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'lievertonh@gmail.com'

        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['lievertonh@gmail.com', 'lievertonh@gmail.com']

        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Lieverton Horn',
            '12345678901',
            'lievertonh@gmail.com',
            '42-3252-1698',
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
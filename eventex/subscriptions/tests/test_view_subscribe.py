from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscriptionGet(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')
        self.form = self.response.context['form']


    def test_get(self):
        '''Get /inscricao/ Must return 200 '''
        self.response = self.client.get('/inscricao/')
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        '''Must use subscriptions/subscription_form.html'''
        self.response = self.client.get('/inscricao/')
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        '''Html must contain input tags'''
        tags = [('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1)]

        for text, count in tags:
           with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        '''Must contain csrf token'''
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        '''Must contain a Subscription form'''
        self.assertIsInstance(self.form, SubscriptionForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Lieverton Horn', cpf='12345678901',
                    email='lievertonh@gmail.com', phone='42-3252-1698')
        self.response = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_post(self):
        '''valid post should redirect to /inscircao/'''
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))


class SubscribePostnvalid(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})
        self.form = self.response.context['form']

    def test_post(self):
        '''Invalid POST, should not redirect'''

        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        '''Must contain a Subscription form'''
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_errors(self):
        self.assertTrue(self.form.errors)


class SubscribeSucessMessage(TestCase):
    def test_message(self):
        data = dict(name='Lieverton Horn', cpf='12345678901',
                        email='lievertonh@gmail.com', phone='42-3252-1698')

        response = self.client.post('/inscricao/', data, follow=True)

        self.assertContains(response, 'Inscrição realizada com sucesso!')
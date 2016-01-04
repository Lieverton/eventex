from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscriptionTest(TestCase):
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
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        '''Must contain csrf token'''
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        '''Must contain a Subscription form'''
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_fields(self):
        '''Form must contain fields'''
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(self.form.fields))


class SubscribePostTest(TestCase):
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

        self.assertIn('Lieverton Horn', self.email.body)
        self.assertIn('12345678901', self.email.body)
        self.assertIn('lievertonh@gmail.com', self.email.body)
        self.assertIn('42-3252-1698', self.email.body)


class SubscribeInvalidPost(TestCase):
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
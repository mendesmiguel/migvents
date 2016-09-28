from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = SubscriptionForm()
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digit(self):
        form = self.make_form(cpf='ABCD')
        self.assertFromErrorCode(form, 'cpf', 'digit')

    def test_cpf_must_have_11_digits(self):
        form = self.make_form(cpf='1234')
        self.assertFromErrorCode(form, 'cpf', 'length')

    def test_name_must_be_capitalized(self):
        form = self.make_form(name='MANCEbo legal')
        self.assertEqual('Mancebo Legal', form.cleaned_data['name'])

    def test_email_is_optional(self):
        form = self.make_form(email='')
        self.assertFalse(form.errors)

    def test_phone_is_optional(self):
        form = self.make_form(phone='')
        self.assertFalse(form.errors)

    def test_must_have_either_email_or_phone(self):
        form = self.make_form(phone='', email='')
        self.assertListEqual(['__all__'], list(form.errors))

    def assertFromErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def make_form(self, **kwargs):
        valid = dict(name='Mancebo Legal',
                    cpf='12345678901',
                    email='mancebo@legal.com',
                    phone='21 2222-3333')

        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()
        return form

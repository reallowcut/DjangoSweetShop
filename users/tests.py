from django.test import TestCase, Client
from django.urls import reverse


class UserRegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_post_valid_form(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code,
                         302)
        self.assertRedirects(response, reverse('login'))

    def test_register_view_post_invalid_form(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': '',
            'email': 'johndoe@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        }
        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertTrue('username' in form.errors)
        self.assertEqual(form.errors['username'], ['Обязательное поле.'])

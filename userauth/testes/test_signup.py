from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupViewTests(TestCase):
    def test_signup_page_status_code(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_signup_form(self):
        url = reverse('signup')
        data = {
            'username': 'testuser',
            'email': 'teste@example.com',
            'password1': 'complexPassword123',
            'password2': 'complexPassword123',
        }
        response = self.client.post(url, data)
        # Após cadastro, deve redirecionar (302)
        self.assertEqual(response.status_code, 302)
        # Verifica se usuário foi criado no banco
        user_exists = User.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)
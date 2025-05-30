from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='complexPassword123',
            full_name='Test User'
        )

    def test_login_page_status_code(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'complexPassword123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # redireciona após login
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_fail(self):
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # sem redirecionamento
        self.assertContains(response, "Usuário ou senha inválidos")  # ajuste conforme sua mensagem real

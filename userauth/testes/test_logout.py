from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class LogoutViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='logoutuser',
            email='logout@example.com',
            password='ComplexPass123',
            full_name='Logout User'
        )
        self.client.login(username='logoutuser', password='ComplexPass123')

    def test_logout_redirects(self):
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

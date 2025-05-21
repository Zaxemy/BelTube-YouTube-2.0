from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
import json

class UserViewsTestCase(APITestCase):
    """Тесты для views приложения users"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        cls.client = APIClient()

    def test_user_registration(self):
        """Тест регистрации нового пользователя"""
        url = reverse('users:register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        """Тест авторизации пользователя"""
        url = reverse('users:login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_user_profile_unauthorized(self):
        """Тест доступа к профилю без авторизации"""
        url = reverse('users:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_authorized(self):
        """Тест доступа к профилю с авторизацией"""
        self.client.force_authenticate(user=self.user)
        url = reverse('users:profile')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_subscription_flow(self):
        """Тест полного цикла подписки"""
        # Создаем второго пользователя
        user2 = User.objects.create_user(username='user2', password='pass2')
        
        # Авторизуемся как первый пользователь
        self.client.force_authenticate(user=self.user)
        
        # Подписываемся
        subscribe_url = reverse('users:user-subscribe', kwargs={'pk': user2.id})
        response = self.client.post(subscribe_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Проверяем список подписок
        subscriptions_url = reverse('users:user-subscriptions')
        response = self.client.get(subscriptions_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'user2')
        
        # Отписываемся
        response = self.client.delete(subscribe_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
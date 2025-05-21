from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError
from users.models import User
from users.serializers import RegisterSerializer, UserSerializer
import os


class UserSerializersTestCase(TestCase):
    """Тестируем все сериализаторы пользователей"""

    @classmethod
    def setUpTestData(cls):
        # Общие данные для всех тестов
        cls.valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        }
        
        # Тестовый файл аватара
        cls.avatar_file = SimpleUploadedFile(
            name='test_avatar.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00',
            content_type='image/jpeg'
        )

    def tearDown(self):
        # Удаляем тестовые файлы после каждого теста
        for user in User.objects.all():
            if user.avatar and os.path.exists(user.avatar.path):
                os.remove(user.avatar.path)

    # Тесты для RegisterSerializer
    def test_register_serializer_valid_data(self):
        """Тест успешной регистрации с валидными данными"""
        serializer = RegisterSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('ComplexPass123!'))

    def test_register_serializer_password_mismatch(self):
        """Тест ошибки при несовпадении паролей"""
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'WrongPassword'
        
        serializer = RegisterSerializer(data=invalid_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        
        self.assertIn('Пароли не совпадают', str(context.exception))

    def test_register_serializer_weak_password(self):
        """Тест валидации сложности пароля"""
        weak_data = self.valid_data.copy()
        weak_data['password'] = '123'
        weak_data['password2'] = '123'
        
        serializer = RegisterSerializer(data=weak_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        
        self.assertIn('Слишком простой пароль', str(context.exception))

    # Тесты для UserSerializer
    def test_user_serializer_output(self):
        """Тест корректности выходных данных UserSerializer"""
        user = User.objects.create_user(
            username='serializer_test',
            password='testpass123',
            email='serializer@test.com',
            bio='Test bio'
        )
        user.avatar = self.avatar_file
        user.save()
        
        serializer = UserSerializer(instance=user)
        data = serializer.data
        
        self.assertEqual(data['username'], 'serializer_test')
        self.assertEqual(data['bio'], 'Test bio')
        self.assertIn('test_avatar.jpg', data['avatar'])
        self.assertFalse(data['is_subscribed'])  # По умолчанию False

    def test_user_serializer_subscription_logic(self):
        """Тест работы поля is_subscribed"""
        user1 = User.objects.create_user(username='user1', password='pass1')
        user2 = User.objects.create_user(username='user2', password='pass2')
        
        # Подписываем user1 на user2
        user2.subscribers.add(user1)
        
        # Сериализуем user2 для user1 (должен показать is_subscribed=True)
        serializer = UserSerializer(
            instance=user2,
            context={'request': self._create_request_with_user(user1)}
        )
        self.assertTrue(serializer.data['is_subscribed'])

    # Вспомогательные методы
    def _create_request_with_user(self, user):
        """Создает фейковый request с пользователем для контекста"""
        from rest_framework.test import APIRequestFactory
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = user
        return request
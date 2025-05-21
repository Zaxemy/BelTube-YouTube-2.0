from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User
import os


class UserModelTestCase(TestCase):
    """Тестируем модель User"""
    
    @classmethod
    def setUpTestData(cls):
        """
        Настройка тестовых данных. Выполняется один раз перед всеми тестами.
        Здесь создаем пользователей для тестирования.
        """
        # Основной тестовый пользователь
        cls.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123',
            bio='Тестовое био'
        )
        
        # Второй пользователь для тестирования подписок
        cls.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com'
        )
        
        # Создаем тестовый аватар
        cls.avatar = SimpleUploadedFile(
            name='test_avatar.jpg',
            content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00',  # Просто бинарные данные имитирующие картинку
            content_type='image/jpeg'
        )

    def test_user_creation(self):
        
        """Тест базового создания пользователя"""
        self.assertEqual(self.user1.username, 'testuser1')
        self.assertEqual(self.user1.email, 'test1@example.com')
        self.assertEqual(self.user1.bio, 'Тестовое био')
        self.assertTrue(self.user1.check_password('testpass123'))
        
    def test_avatar_upload(self):
        
        """Тест загрузки аватара"""
        self.user1.avatar = self.avatar
        self.user1.save()
        
        self.assertTrue(self.user1.avatar)  # Проверяем что аватар установлен
        self.assertIn('users_avatars/test_avatar', self.user1.avatar.path)
        
        # Удаляем тестовый файл после проверки
        if os.path.exists(self.user1.avatar.path):
            os.remove(self.user1.avatar.path)

    def test_subscribers_relationship(self):
        
        """Тест системы подписчиков"""
        # user1 подписывается на user2
        self.user2.subscribers.add(self.user1)
        
        # Проверяем подписчиков user2
        self.assertEqual(self.user2.subscribers.count(), 1)
        self.assertIn(self.user1, self.user2.subscribers.all())
        
        # Проверяем подписки user1
        self.assertEqual(self.user1.subscriptions.count(), 1)
        self.assertIn(self.user2, self.user1.subscriptions.all())

    def test_subscribers_count_property(self):
        """Тест вычисляемого поля subscribers_count"""
        self.user2.subscribers.add(self.user1)
        self.assertEqual(self.user2.subscribers_count, 1)

    def test_subscriptions_count_property(self):
        """Тест вычисляемого поля subscriptions_count"""
        self.user1.subscriptions.add(self.user2)
        self.assertEqual(self.user1.subscriptions_count, 1)

    def test_str_representation(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.user1), 'testuser1')
        # Создаем нового пользователя с паролем
        new_user = User.objects.create_user(
            username='john',
            password='testpass123'
        )
        self.assertEqual(str(new_user), 'john')

    def tearDown(self):
        """Очистка после каждого теста"""
        # Удаляем все аватары, созданные во время тестов
        for user in User.objects.all():
            if user.avatar and os.path.exists(user.avatar.path):
                os.remove(user.avatar.path)
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from videos.models import Video, Like

class VideoViewsTestCase(APITestCase):
    """Тесты для views приложения videos"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        cls.video = Video.objects.create(
            title='Test Video',
            author=cls.user
        )
        cls.client = APIClient()

    def test_video_list(self):
        """Тест получения списка видео"""
        url = reverse('videos:video-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_video_detail(self):
        """Тест получения конкретного видео"""
        url = reverse('videos:video-detail', kwargs={'pk': self.video.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Video')

    def test_video_like_unauthorized(self):
        """Тест лайка без авторизации"""
        url = reverse('videos:video-like', kwargs={'pk': self.video.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_video_like_flow(self):
        """Тест полного цикла лайка"""
        self.client.force_authenticate(user=self.user)
        url = reverse('videos:video-like', kwargs={'pk': self.video.id})
        
        # Ставим лайк
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'liked')
        self.assertEqual(Like.objects.count(), 1)
        
        # Убираем лайк
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'unliked')
        self.assertEqual(Like.objects.count(), 0)

    def test_video_upload(self):
        """Тест загрузки видео"""
        self.client.force_authenticate(user=self.user)
        url = reverse('videos:video-list')
        
        with open('test_video.mp4', 'rb') as video_file:
            data = {
                'title': 'Uploaded Video',
                'video_file': video_file
            }
            response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Video.objects.filter(title='Uploaded Video').exists())
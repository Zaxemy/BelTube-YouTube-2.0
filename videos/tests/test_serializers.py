from django.test import TestCase
from rest_framework.test import APIRequestFactory
from users.models import User
from videos.models import Video, Comment
from videos.serializers import VideoSerializer, CommentSerializer

class VideoSerializerTestCase(TestCase):
    """Тесты для VideoSerializer"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.video = Video.objects.create(
            title='Serializer Test',
            author=cls.user
        )
        cls.factory = APIRequestFactory()

    def test_video_serializer_data(self):
        """Тест данных сериализатора"""
        request = self.factory.get('/')
        request.user = self.user
        
        serializer = VideoSerializer(
            instance=self.video,
            context={'request': request}
        )
        
        data = serializer.data
        self.assertEqual(data['title'], 'Serializer Test')
        self.assertEqual(data['author']['username'], 'testuser')
        self.assertEqual(data['likes_count'], 0)
        self.assertFalse(data['is_liked'])

    def test_video_serializer_like_status(self):
        """Тест статуса лайка"""
        # Создаем второго пользователя и лайк
        user2 = User.objects.create_user(username='user2', password='pass2')
        self.video.likes.add(user2)
        
        request = self.factory.get('/')
        request.user = user2
        
        serializer = VideoSerializer(
            instance=self.video,
            context={'request': request}
        )
        
        self.assertTrue(serializer.data['is_liked'])

class CommentSerializerTestCase(TestCase):
    """Тесты для CommentSerializer"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='commenter', password='testpass')
        cls.video = Video.objects.create(
            title='Comment Test',
            author=cls.user
        )
        cls.comment = Comment.objects.create(
            text='Test Comment',
            user=cls.user,
            video=cls.video
        )

    def test_comment_serializer_data(self):
        """Тест данных сериализатора"""
        serializer = CommentSerializer(instance=self.comment)
        data = serializer.data
        
        self.assertEqual(data['text'], 'Test Comment')
        self.assertEqual(data['user']['username'], 'commenter')
        self.assertEqual(data['video'], self.video.id)

    def test_comment_replies(self):
        """Тест сериализации ответов"""
        # Создаем ответ на комментарий
        Comment.objects.create(
            text='Reply',
            user=self.user,
            video=self.video,
            parent=self.comment
        )
        
        serializer = CommentSerializer(instance=self.comment)
        self.assertEqual(len(serializer.data['replies']), 1)
        self.assertEqual(serializer.data['replies'][0]['text'], 'Reply')
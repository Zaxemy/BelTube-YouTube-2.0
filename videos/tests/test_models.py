from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User
from videos.models import Video, Comment, Like
import os

class VideoModelTestCase(TestCase):
    """Тесты для модели Video"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='videouser', password='testpass')
        cls.video = Video.objects.create(
            title='Test Video',
            description='Test Description',
            author=cls.user
        )

    def test_video_creation(self):
        """Тест создания видео"""
        self.assertEqual(self.video.title, 'Test Video')
        self.assertEqual(self.video.author.username, 'videouser')
        self.assertEqual(self.video.views, 0)

    def test_video_str_representation(self):
        """Тест строкового представления"""
        self.assertEqual(str(self.video), 'Test Video')

    def test_like_functionality(self):
        """Тест функционала лайков"""
        # Создаем лайк
        like = Like.objects.create(user=self.user, video=self.video)
        self.assertEqual(self.video.likes.count(), 1)
        self.assertEqual(self.user.liked_videos.count(), 1)

class CommentModelTestCase(TestCase):
    """Тесты для модели Comment"""

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

    def test_comment_creation(self):
        """Тест создания комментария"""
        self.assertEqual(self.comment.text, 'Test Comment')
        self.assertEqual(self.comment.user.username, 'commenter')
        self.assertEqual(self.comment.video.title, 'Comment Test')

    def test_reply_comment(self):
        """Тест ответа на комментарий"""
        reply = Comment.objects.create(
            text='Reply Comment',
            user=self.user,
            video=self.video,
            parent=self.comment
        )
        self.assertEqual(self.comment.replies.count(), 1)
        self.assertEqual(reply.parent.text, 'Test Comment')
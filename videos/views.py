from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .models import Video, Like, Comment
from .serializers import VideoSerializer, CommentSerializer
from users.models import User
from django.db import models
from videos.paginations import VideoPagination


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [AllowAny]
    pagination_class = VideoPagination
    
    # Аннотации для оптимизации запросов
    def get_queryset(self):
        user = self.request.user
        return Video.objects.annotate(
            likes_count=models.Count("likes"),
            comments_count=models.Count("comments"),
            is_liked=models.Exists(
                Like.objects.filter(
                    user=user.id if user.is_authenticated else None,
                    video=models.OuterRef("id")
                )
            )
        ).select_related("author")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # Лайк/дизлайк видео
    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        video = self.get_object()
        user = request.user

        if Like.objects.filter(user=user, video=video).exists():
            Like.objects.filter(user=user, video=video).delete()
            return Response({"status": "unliked"})
        else:
            Like.objects.create(user=user, video=video)
            return Response({"status": "liked"}, status=status.HTTP_201_CREATED)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(video_id=self.kwargs["video_pk"])

    def perform_create(self, serializer):
        video = Video.objects.get(id=self.kwargs["video_pk"])
        serializer.save(user=self.request.user, video=video)
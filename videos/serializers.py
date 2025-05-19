from rest_framework import serializers
from .models import Video, Like, Comment
from users.serializers import UserSerializer 




class VideoSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Video
        fields = [
            "id", "title", "description", "video_file", "preview",
            "author", "created_at", "views", "likes_count", "comments_count", "is_liked"
        ]
        read_only_fields = ["author", "created_at", "views"]

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "text", "user", "video", "parent", "replies", "created_at"]
        read_only_fields = ["user", "video", "created_at"]

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []
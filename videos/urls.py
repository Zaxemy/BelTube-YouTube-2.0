from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet, CommentViewSet

app_name = 'videos'


router = DefaultRouter()
router.register(r"videos", VideoViewSet, basename="video")

urlpatterns = [
    path("videos/<int:video_pk>/comments/", CommentViewSet.as_view({
        "get": "list", "post": "create"
    }), name="video-comments"),
    path("", include(router.urls)),
]
from django.db import models
from users.models import User  # Ваша кастомная модель пользователя

class Video(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    video_file = models.FileField(upload_to="videos/", verbose_name="Видеофайл")
    preview = models.ImageField(upload_to="previews/", blank=True, verbose_name="Превью")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ["-created_at"]  # Сортировка по дате

    def __str__(self):
        return self.title   

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["user", "video"]]  # Один лайк от пользователя на видео

class Comment(models.Model):
    text = models.TextField(verbose_name="Текст")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Комментарий от {self.user.username} | Видео: {self.video.title}"
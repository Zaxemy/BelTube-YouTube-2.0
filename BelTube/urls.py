from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


# Настройка документации Swagger/Redoc
schema_view = get_schema_view(
    openapi.Info(
        title="Video Hosting API",
        default_version='v1',
        description="API documentation for Video Hosting Service",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="dev@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Административная панель Django
    path('admin/', admin.site.urls),
    
    # Документация API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints
    path('api/users/', include('users.urls', namespace='users')),
    path('api/videos/', include('videos.urls', namespace='videos')),
]

# Добавляем обработку медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.urls import path
from users.views import *
from rest_framework_simplejwt.views import TokenRefreshView



app_name = 'users'


urlpatterns = [
    
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
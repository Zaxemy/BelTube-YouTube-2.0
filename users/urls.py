from django.urls import path, include
from users.views import RegisterView, LoginView, ProfileView, UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile endpoint
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Subscription endpoints
    path('users/subscriptions/', 
         UserViewSet.as_view({'get': 'subscriptions'}),
         name='user-subscriptions'),
    path('users/<int:pk>/subscribe/', 
         UserViewSet.as_view({'post': 'subscribe', 'delete': 'subscribe'}),
         name='user-subscribe'),
    
    # Include router-generated URLs
    path('', include(router.urls)),
]
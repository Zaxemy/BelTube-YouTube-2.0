from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.decorators import action
from rest_framework import viewsets
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, pk=None):
        author = self.get_object()
        user = request.user
        
        if request.method == 'POST':
            if user in author.subscribers.all():
                return Response({'error': 'Вы уже подписаны'}, status=400)
            author.subscribers.add(user)
            return Response({'status': 'Подписка оформлена'}, status=201)
        
        if request.method == 'DELETE':
            if user not in author.subscribers.all():
                return Response({'error': 'Вы не подписаны'}, status=400)
            author.subscribers.remove(user)
            return Response({'status': 'Подписка отменена'}, status=204)
    
    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        subs = request.user.subscriptions.all()
        serializer = SubscriptionSerializer(
            subs,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Пользователь успешно зарегистрирован"}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username
            })
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'username': request.user.username,
            'email': request.user.email,
            'bio': request.user.bio,
            'avatar': request.user.avatar.url if request.user.avatar else None
        })
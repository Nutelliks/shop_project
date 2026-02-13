from rest_framework import (
    viewsets, generics, permissions, 
    response, status)
from rest_framework_simplejwt import (
    views, tokens
)

from ..models import User
from .serializers import (
    UserSerializer, UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = tokens.RefreshToken.for_user(user)

        return response.Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': "User created successfully"
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(views.TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
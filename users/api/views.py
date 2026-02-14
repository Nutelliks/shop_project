from rest_framework import (
    viewsets, generics, permissions, 
    response, status, views)
from rest_framework_simplejwt import (
    views as jwt_views, tokens as jwt_tokens
)

from ..models import User
from .serializers import (
    UserSerializer, UserRegistrationSerializer,
    CustomTokenObtainPairSerializer, 
    UserProfileSerialier, LogoutSerializer
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

        refresh = jwt_tokens.RefreshToken.for_user(user)

        return response.Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': "User created successfully"
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(jwt_views.TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerialier

    def get_object(self):
        return self.request.user


class LogoutAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return response.Response(
            {"message": "Logout successfully"},
            status=status.HTTP_200_OK
            )
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import UserSerializer, UserCreateSerializer, CustomTokenObtainPairSerializer


class UserCreateView(generics.CreateAPIView):
    """View for creating a new user."""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """View for retrieving and updating user details."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Return the user making the request.
        Admins can view other users' profiles by providing the user ID.
        """
        user_id = self.kwargs.get('pk')
        if user_id and self.request.user.is_staff:
            return generics.get_object_or_404(User, pk=user_id)
        return self.request.user


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token obtain view that includes user details in the response."""
    serializer_class = CustomTokenObtainPairSerializer


class UserListView(generics.ListAPIView):
    """View for listing all users (admin only)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

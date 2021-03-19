from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from users.serializers import UserSerializer

User = get_user_model()


class CreateUserView(mixins.CreateModelMixin, GenericViewSet):
    """Регистрация пользователя."""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

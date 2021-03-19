from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class UserSerializer(ModelSerializer):
    """Сериалайзер регистрации."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password',)

    def create(self, validated_data):
        """Сохранение пользователи в модели User."""
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

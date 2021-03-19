from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class WithNoUpdate(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """Кастомный ViewSet."""
    pass


class WithNoUpdateCreate(mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """Кастомный ViewSet."""
    pass
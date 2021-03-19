from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .costom_viewset import WithNoUpdate, WithNoUpdateCreate
from .models import Wallet, Transaction
from .permissions import (WalletIsOwnerOrAdmin, TransactionsIsOwnerOrAdmin)
from .serializers import (WalletSerializer, WalletTransactionSerializer,
                          UserTransactionSerializer)
from .utils import transaction_canceling, operation_with_money


class WalletViewSet(ModelViewSet):
    """Кошельки"""
    permission_classes = (WalletIsOwnerOrAdmin,)
    serializer_class = WalletSerializer

    def get_queryset(self):
        queryset = Wallet.objects.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WalletTransactionViewSet(WithNoUpdate):
    """Транзакции по кошельку"""
    permission_classes = (TransactionsIsOwnerOrAdmin,)
    serializer_class = WalletTransactionSerializer

    def get_queryset(self):
        my_user = self.request.user
        wallet = get_object_or_404(Wallet, id=self.kwargs['wallet_id'])
        if wallet.owner != my_user:
            raise ValidationError({'403 Forbidden': 'доступ закрыт'})
        queryset = wallet.transactions.all()
        return queryset

    def perform_create(self, serializer):
        wallet = get_object_or_404(Wallet, id=self.kwargs['wallet_id'])
        result = operation_with_money(serializer.validated_data, wallet)
        if not result:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer.save(wallet=wallet)

    def destroy(self, request, *args, **kwargs):
        transaction = self.get_object()
        wallet = transaction.wallet
        transaction_canceling(transaction, wallet)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserTransactionViewSet(WithNoUpdateCreate):
    """Все транзакции пользователя."""
    permission_classes = (TransactionsIsOwnerOrAdmin,)
    serializer_class = UserTransactionSerializer

    def get_queryset(self):
        my_user = self.request.user
        queryset = Transaction.objects.filter(wallet__owner=my_user)
        return queryset

    def destroy(self, request, *args, **kwargs):
        transaction = self.get_object()
        wallet = transaction.wallet
        transaction_canceling(transaction, wallet)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

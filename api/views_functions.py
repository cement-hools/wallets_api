from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Wallet, Transaction
from .serializers import (WalletSerializer, WalletTransactionSerializer,
                          UserTransactionSerializer)
from .utils import transaction_canceling, operation_with_money

User = get_user_model()


@api_view(['GET', 'POST'])
def wallets(request):
    """Список всех кошельков и создание нового."""
    my_user = request.user
    if request.method == 'GET':
        wallets = Wallet.objects.filter(owner=my_user)
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=my_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
def wallet_detail(request, wallet_id):
    """Управление кошельком (просмотр, редактирование, удаление)."""
    my_user = request.user
    wallet = get_object_or_404(Wallet, id=wallet_id)
    if wallet.owner != my_user:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = WalletSerializer(wallet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        wallet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def wallet_transactions(request, wallet_id):
    """Проведение транзакции и список всех транзакций по кошельку."""
    my_user = request.user
    my_wallet = get_object_or_404(Wallet, id=wallet_id)
    if my_wallet.owner != my_user:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        transactions = my_wallet.transactions.all()
        serializer = WalletTransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = WalletTransactionSerializer(data=request.data)
        if serializer.is_valid():
            result = operation_with_money(serializer.validated_data, my_wallet)
            if not result:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            serializer.save(wallet=my_wallet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def wallet_transactions_detail(request, wallet_id, transaction_id):
    """Просмотр транзакции и ее удаление с востанавлением баланса на кошельке."""
    my_user = request.user
    my_wallet = get_object_or_404(Wallet, id=wallet_id)
    if my_wallet.owner != my_user:
        return Response(status=status.HTTP_403_FORBIDDEN)
    transaction = my_wallet.transactions.filter(id=transaction_id).first()
    if request.method == 'GET':
        serializer = WalletTransactionSerializer(transaction)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        transaction_canceling(transaction, my_wallet)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def transactions(request):
    """список всех транзакций."""
    my_user = request.user
    transactions = Transaction.objects.filter(wallet__owner=my_user)
    if request.method == 'GET':
        serializer = UserTransactionSerializer(transactions, many=True)
        return Response(serializer.data)

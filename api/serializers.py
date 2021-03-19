from rest_framework import serializers

from .models import Wallet, Transaction


class UserTransactionSerializer(serializers.ModelSerializer):
    wallet = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        fields = '__all__'
        model = Transaction
        read_only_fields = ('id', 'balance', 'created',)


class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('wallet',)
        model = Transaction
        read_only_fields = ('id', 'balance', 'created',)


class WalletSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    transactions = WalletTransactionSerializer(many=True, read_only=True)

    class Meta:
        fields = ('id', 'title', 'owner', 'description', 'balance', 'created',
                  'transactions',)
        model = Wallet
        read_only_fields = ('id', 'owner', 'balance',)

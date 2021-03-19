from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views_classes import (WalletViewSet, WalletTransactionViewSet,
                            UserTransactionViewSet)
from .views_functions import (wallets, wallet_transactions, transactions,
                              wallet_detail, wallet_transactions_detail)

wallet_router = DefaultRouter()
wallet_router.register('wallets', WalletViewSet, basename='wallets')

transaction_router = DefaultRouter()
transaction_router.register('transactions', WalletTransactionViewSet,
                            basename='transactions')

transactions_all_router = DefaultRouter()
transactions_all_router.register('transactions_all', UserTransactionViewSet,
                                 basename='user_transactions')

urlpatterns = [

    path('v1/wallets/', wallets, name='wallets'),
    path('v1/wallet/<int:wallet_id>/', wallet_detail, name='wallet_detail'),
    path('v1/wallet/<int:wallet_id>/transactions/', wallet_transactions,
         name='wallet_transactions'),
    path('v1/wallet/<int:wallet_id>/transaction/<int:transaction_id>',
         wallet_transactions_detail,
         name='wallet_transactions_detail'),
    path('v1/transactions/', transactions, name='transactions'),

    path('v2/', include(wallet_router.urls)),
    path('v2/', include(transactions_all_router.urls)),
    path('v2/wallets/<int:wallet_id>/', include(transaction_router.urls)),

]

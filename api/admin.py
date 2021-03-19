from django.contrib import admin

from api.models import Transaction, Wallet


class WalletAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'balance', 'created',)
    list_filter = ('title', 'owner',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'type', 'amount', 'created',)
    list_filter = ('wallet', 'wallet__owner', 'type', 'created',)


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction, TransactionAdmin)

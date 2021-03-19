from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Wallet(models.Model):
    """Кошелек пользователя."""
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', null=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wallets',
        verbose_name='Собственник',
    )
    balance = models.DecimalField('Баланс', default=0, max_digits=18,
                                  decimal_places=2)

    created = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошельки'
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Transaction(models.Model):
    """Транзакции по кошельку."""
    TYPE_TRANSACTION = (
        ('+', 'Зачисление'),
        ('-', 'Списание'),
    )
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Кошелек',
    )
    type = models.CharField('Тип транзакции', choices=TYPE_TRANSACTION,
                            max_length=16, null=False)
    comment = models.TextField('Комментарий')
    amount = models.DecimalField('Сумма', null=False, max_digits=18,
                                 decimal_places=2)

    created = models.DateTimeField('Дата совершения транзакции',
                                   auto_now_add=True)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ('-created',)

    def __str__(self):
        wallet = self.wallet.title

        return f'{wallet}: {self.type}{self.amount}'

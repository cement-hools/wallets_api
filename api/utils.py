def operation_with_money(validated_data, wallet):
    def crediting(wallet, amount):
        wallet.balance += amount
        wallet.save()
        return True

    def debiting(wallet, amount):
        if wallet.balance < amount:
            return False
        wallet.balance -= amount
        wallet.save()
        return True
    
    amount = validated_data['amount']
    type_operation = validated_data['type']

    operations = {
        '+': lambda x, y: crediting(x, y),
        '-': lambda x, y: debiting(x, y),
    }
    return operations[type_operation](wallet, amount)


def transaction_canceling(transaction, wallet):
    if transaction.type == '-':
        wallet.balance += transaction.amount
        wallet.save()
    elif transaction.type == '+':
        wallet.balance -= transaction.amount
        wallet.save()
    return True

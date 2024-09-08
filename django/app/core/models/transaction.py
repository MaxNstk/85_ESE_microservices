from django.db import models
from django.utils import timezone


class TransactionType(models.TextChoices):
    EXPENSE = "EXPENSE", "Despesa"
    INCOME = "INCOME", "Receita"

class Transaction(models.Model):
    account = models.ForeignKey("Account", on_delete=models.DO_NOTHING, verbose_name='Conta')
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices, verbose_name='Tipo de Transação')
    date = models.DateTimeField(default=timezone.now, verbose_name='Data')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Valor')
    description = models.CharField(max_length=255, verbose_name='Descrição')
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True, verbose_name='Recibo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    def __str__(self):
        return f"{self.account} - {self.amount} - {self.date}"

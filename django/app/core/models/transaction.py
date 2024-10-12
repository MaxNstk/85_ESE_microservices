from django.db import models
from django.utils import timezone

from .base_model import BaseModel

 
class TransactionType(models.TextChoices):
    EXPENSE = "EXPENSE", "Despesa"
    INCOME = "INCOME", "Receita"

class Transaction(BaseModel):
    account = models.ForeignKey("Account", on_delete=models.DO_NOTHING, verbose_name='Conta')
    category = models.ForeignKey("Category", on_delete=models.DO_NOTHING, verbose_name='Categoria')

    description = models.CharField(max_length=255, verbose_name='Descrição')
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices, verbose_name='Tipo de Transação')
    date = models.DateTimeField(default=timezone.now, verbose_name='Data')
    value = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Valor')
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True, verbose_name='Recibo')

    def __str__(self):
        return f"{self.account} - {self.value} - {self.date}"

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"
        
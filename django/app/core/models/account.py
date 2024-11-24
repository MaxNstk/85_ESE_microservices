from django.db import models
from django.conf import settings
from .base_model import BaseModel


class AccountType(models.TextChoices):
    CHECKING = "CHECKING", "Corrente"
    SAVINGS = "SAVINGS", "Poupança"
 

class Account(BaseModel):
    bank_name = models.CharField(max_length=50, verbose_name='Nome do Banco')
    account_number = models.CharField(max_length=20, verbose_name='Número da Conta', unique=True)
    account_type = models.CharField(max_length=10, choices=AccountType.choices, default=AccountType.CHECKING, verbose_name='Tipo de Conta')
    branch_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='Código da Agência')
    
    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"
    
    class Meta:
        verbose_name = "Conta"
        verbose_name_plural = "Contas"
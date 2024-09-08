from django.db import models
from django.conf import settings


class AccountType(models.TextChoices):
    CHECKING = "CHECKING", "Corrente"
    SAVINGS = "SAVINGS", "Poupança"

class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name='Usuário')
    bank_name = models.CharField(max_length=50, verbose_name='Nome do Banco')
    account_number = models.CharField(max_length=20, verbose_name='Número da Conta', unique=True)
    account_type = models.CharField(max_length=10, choices=AccountType.choices, default=AccountType.CHECKING, verbose_name='Tipo de Conta')
    branch_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='Código da Agência')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')
    
    def __str__(self):
        return f"({self.user.username}) {self.bank_name} - {self.account_number}"
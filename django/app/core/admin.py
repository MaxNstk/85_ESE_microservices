from django.contrib import admin
from .models import Account, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'bank_name', 'account_number', 'account_type', 'branch_code', 'created_at', 'updated_at')
    search_fields = ('user__username', 'bank_name', 'account_number', 'branch_code')
    list_filter = ('account_type',)
    ordering = ['bank_name', 'account_number'] 

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'date', 'value', 'description', 'receipt', 'created_at', 'updated_at')
    search_fields = ('account__account_number', 'date', 'description')
    list_filter = ('transaction_type',)
    ordering = ('-date',) 

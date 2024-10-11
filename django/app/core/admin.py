from django.contrib import admin
from .models import Account, Transaction, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'account_number', 'account_type', 'branch_code', 'created_at', 'updated_at')
    search_fields = ('bank_name', 'account_number', 'branch_code')
    list_filter = ('account_type',)
    ordering = ['bank_name', 'account_number'] 


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'date', 'value', 'description', 'receipt', 'created_at', 'updated_at')
    search_fields = ('account__account_number', 'date', 'description')
    list_filter = ('transaction_type',)
    ordering = ('-date',) 

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Account, Transaction, Category, User
from django.contrib.auth.admin import UserAdmin
import requests

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
    readonly_fields = ['generate_pdf_button']

    def generate_pdf_button(self, obj):
        if obj.pk: 
            url = f"{reverse('gerar_pdf')}?account_number={obj.account_number}"
            return format_html(f'<a class="button" href="{url}" target="_blank">Gerar Relatório de Transações</a>')
        return "Salve a conta para gerar o relatório."
    
    generate_pdf_button.short_description = "Gerar Relatório PDF"

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'date', 'value', 'description', 'receipt', 'created_at', 'updated_at')
    search_fields = ('account__account_number', 'date', 'description')
    list_filter = ('transaction_type',)
    ordering = ('-date',) 


@admin.register(User)
class UserAdmin(UserAdmin):

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("full_name", "username", "password1", "password2"),
            },
        ),
    )
    
    def response_add(self, request, obj, **kwargs): 
        res = super().response_add(request, obj, **kwargs ) 
        response = requests.post('http://authentication:3000/',data={'username':'admin','password':'admin'})
        response_data = response.json()
        requests.post('http://authentication:3000/users/', 
            data={"username":request.POST['username'], "password":request.POST['password1'], "fullName":request.POST['full_name']}, 
            headers={'Authorization': f'Bearer {response_data['jwt']}'}
        )
        return res
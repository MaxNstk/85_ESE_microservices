from django.test import TestCase
from django.utils import timezone
from app.core.models import Account, Category, Transaction, User
import os
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


class AccountTestCase(TestCase):
    
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='password', full_name='Test User')

        self.account = Account.objects.create(
            bank_name="Bank of Test",
            account_number="1234567890",
            account_type="CHECKING",
            branch_code="0001"
        )

        self.category = Category.objects.create(
            name="Food",
            description="Expenses related to food and groceries"
        )

        self.transaction = Transaction.objects.create(
            account=self.account,
            category=self.category,
            description="Grocery Shopping",
            transaction_type="EXPENSE",
            date=timezone.now(),
            value=100.00,
        )

    def test_account_creation(self):
        account = Account.objects.get(account_number="1234567890")
        self.assertEqual(account.bank_name, "Bank of Test")
        self.assertEqual(account.account_type, "CHECKING")

    def test_category_creation(self):
        category = Category.objects.get(name="Food")
        self.assertEqual(category.description, "Expenses related to food and groceries")

    def test_transaction_creation(self):
        transaction = Transaction.objects.get(description="Grocery Shopping")
        self.assertEqual(transaction.value, 100.00)
        self.assertEqual(transaction.transaction_type, "EXPENSE")
        self.assertEqual(transaction.account, self.account)
        self.assertEqual(transaction.category, self.category)


class PDFTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', full_name='Test User')

        self.account = Account.objects.create(
            bank_name="Bank of Test",
            account_number="1234567890",
            account_type="CHECKING",
            branch_code="0001"
        )

        self.category = Category.objects.create(
            name="Utilities",
            description="Expenses related to utility bills"
        )

    def test_generate_pdf_with_receipt(self):
        pdf_path = os.path.join(os.path.dirname(__file__), 'test.pdf')
        with open(pdf_path, 'rb') as pdf_file:
            uploaded_pdf = SimpleUploadedFile("test.pdf", pdf_file.read(), content_type="application/pdf")
            
            Transaction.objects.create(
                account=self.account,
                category=self.category,
                description="Utility Bill Payment",
                transaction_type="EXPENSE",
                date=timezone.now(),
                value=150.00,
                receipt=uploaded_pdf
            )

        response = self.client.get(reverse('gerar_pdf'), {'account_number': self.account.account_number})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn("attachment; filename=\"relatorio_extrato_financeiro.pdf\"", response['Content-Disposition'])

from django.utils import timezone
from app.core.models import Transaction
from .base_report_generator import BaseReportGenerator
import requests
import base64

class PDFReportGenerator(BaseReportGenerator):
    def fetch_transactions(self, account):
        return Transaction.objects.filter(account=account)

    def build_context(self, account, transactions):
        transactions = self.convert_pdf_to_image(transactions)
        return {
            'title': 'Relatório de Extratos Financeiros',
            'request_date': timezone.now(),
            'account': account,
            'transactions': transactions,
        }

    def convert_pdf_to_image(self, transactions):
        for transaction in transactions:
            if transaction.receipt:
                with transaction.receipt.open('rb') as file:
                    files = {"file": ("arquivo.pdf", file, "application/pdf")}
                    response = requests.post("http://localhost:81/pdfToImage/v1/upload-pdf/?response_format=png", files=files)

                    if response.status_code == 200:
                        image_data = base64.b64encode(response.content).decode("utf-8")
                        transaction.receipt_base64 = image_data
                    else:
                        print(f"Erro ao enviar PDF: {response.status_code}, {response.text}")
                        transaction.receipt_base64 = None
            else:
                transaction.receipt_base64 = None

        return transactions

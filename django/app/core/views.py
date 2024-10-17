# views.py

import base64
import requests
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from xhtml2pdf import pisa

from .models import Transaction, Account

def gerar_pdf(request):

    account_number  = request.GET.get('account_number')

    if account_number :
        account = get_object_or_404(Account, account_number=account_number)
        transactions = Transaction.objects.filter(account=account)
    else:
        return HttpResponse("Número da conta não fornecido.", status=400)
    
    transactions = convert_pdf_to_image(transactions) 

    context = {
        'title': 'Relatório de Extratos Financeiros',
        'request_date': timezone.now(),
        'account': account,
        'transactions': transactions,
    }

    html = render_to_string('relatorio_extrato_financeiro.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_extrato_financeiro.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)

    return response

def convert_pdf_to_image(transactions):
    for transaction in transactions:
        if transaction.receipt:
            with transaction.receipt.open('rb') as file:
                files = {"file": ("arquivo.pdf", file, "application/pdf")}
                response = requests.post("http://localhost:81/pdfToImage/v1/upload-pdf/", files=files)

                if response.status_code == 200:
                    image_data = base64.b64encode(response.content).decode("utf-8")
                    transaction.receipt_base64 = image_data
                else:
                    print(f"Erro ao enviar PDF: {response.status_code}, {response.text}")
                    transaction.receipt_base64 = None
        else:
            transaction.receipt_base64 = None

    return transactions
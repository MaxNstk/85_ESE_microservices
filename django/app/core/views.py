# views.py

import requests
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from xhtml2pdf import pisa

from app.core.models.transaction import Transaction

def gerar_pdf(request):

    transacoes = convert_pdf_to_image(Transaction.objects.all()) 

    context = {
        'titulo': 'Relatório de Extratos Financeiros',
        'data_emissao': timezone.now(),
        'transacoes': transacoes,
    }

    html = render_to_string('relatorio_extrato_financeiro.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_extrato_financeiro.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)

    return response

def convert_pdf_to_image(transacoes):

    for transacao in transacoes:
        if transacao.receipt:

            with transacao.receipt.open('rb') as file:
                files = {"file": (transacao.receipt.name, file, "application/pdf")}
                response = requests.post("http://localhost:8001/v1/upload-pdf/", files=files)

                if response.status_code == 200:
                    transacao.receipt_base64 = response.json().get("images", [])
                else:
                    print(f"Erro ao enviar PDF: {response.status_code}, {response.text}")
                    transacao.receipt_base64 = None
        else:
            transacao.receipt_base64 = None

    return transacoes
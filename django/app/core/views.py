# views.py

import base64
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from xhtml2pdf import pisa

from app.core.models.transaction import Transaction

def gerar_pdf(request):

    transacoes = Transaction.objects.all() 

    for transacao in transacoes:
        if transacao.receipt:
            with transacao.receipt.open('rb') as file:
                receipt_content = file.read()
                transacao.receipt_base64 = base64.b64encode(receipt_content).decode('utf-8')
        else:
            transacao.receipt_base64 = None 

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
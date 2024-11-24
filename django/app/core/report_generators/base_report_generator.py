from abc import ABC, abstractmethod
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse
from app.core.models import Account

class BaseReportGenerator(ABC):
    def generate_report(self, request):
        account_number = request.GET.get('account_number')
        if account_number:
            account = get_object_or_404(Account, account_number=account_number)
            transactions = self.fetch_transactions(account)
            context = self.build_context(account, transactions)
            response = self.create_response(context)
            return response
        return HttpResponse("Número da conta não fornecido.", status=400)

    @abstractmethod
    def fetch_transactions(self, account):
        pass

    @abstractmethod
    def build_context(self, account, transactions):
        pass

    def create_response(self, context):
        html = self.render_to_string(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_extrato_financeiro.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Erro ao gerar PDF', status=500)
        return response

    def render_to_string(self, context):
        return render_to_string('relatorio_extrato_financeiro.html', context)

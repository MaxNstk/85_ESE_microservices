from django.http import HttpResponse
from .report_generators.pdf_report_generator import PDFReportGenerator

def gerar_pdf(request):
    report_generator = PDFReportGenerator()
    return report_generator.generate_report(request)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Func, IntegerField
from datetime import datetime, timedelta
from empresa.models import Empresa
from colaborador.models import Colaborador
from equipamento.models import Equipamento


class ExtractYear(Func):
    function = 'EXTRACT'
    template = '%(function)s(YEAR FROM %(expressions)s)'
    output_field = IntegerField()

class ExtractMonth(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH FROM %(expressions)s)'
    output_field = IntegerField()

class EmpresasCadastradasNosUltimos12Meses(APIView):
    def get(self, request, format=None):
        today = datetime.now()
        twelve_months_ago = today - timedelta(days=365)

        all_months = [(twelve_months_ago + timedelta(days=30 * i)).strftime('%Y-%m') for i in range(1, 13)]
        all_months.reverse()  # Invertendo a ordem da lista

        empresas_cadastradas = (
            Empresa.objects
            .annotate(year=ExtractYear('data_cadastro'), month=ExtractMonth('data_cadastro'))
            .values('year', 'month')
            .annotate(total=Count('id'))
            .order_by('year', 'month')
        )

        result = []
        for month in all_months:
            year, month = map(int, month.split('-'))
            entry = next((entry for entry in empresas_cadastradas if entry['year'] == year and entry['month'] == month), {'total': 0})
            result.append({
                'ano': year,
                'mes': month,
                'total': entry['total']
            })

        return Response(result)


class ColaboradoresCadastradosNosUltimos12Meses(APIView):
    def get(self, request, format=None):
        today = datetime.now()
        twelve_months_ago = today - timedelta(days=365)
    
        all_months = [(twelve_months_ago + timedelta(days=30 * i)).strftime('%Y-%m') for i in range(1,13)]
        all_months.reverse() # Invertendo a ordem da lista

        colaboradores_cadastrados = (
            Colaborador.objects
            .annotate(year=ExtractYear('data_cadastro'), month=ExtractMonth('data_cadastro'))
            .values('year', 'month')
            .annotate(total=Count('id'))
            .order_by('year', 'month')
        )

        result = []
        for month in all_months:
            year, month = map(int, month.split('-'))
            entry = next((entry for entry in colaboradores_cadastrados if entry['year'] == year and entry['month'] == month), {'total': 0})
            result.append({
                'ano': year,
                'mes': month,
                'total': entry['total']
            })
        
        return Response(result)
    

class EquipamentosCadastradosNosUltimos12Meses(APIView):
    def get(self, request, format=None):
        today = datetime.now()
        twelve_months_ago = today - timedelta(days=365)

        all_months = [(twelve_months_ago + timedelta(days=30 * i)).strftime('%Y-%m') for i in range(1, 13)]
        all_months.reverse() # Invertendo a ordem da lista

        equipamentos_cadastrados = (
            Equipamento.objects
            .annotate(year=ExtractYear('data_cadastro'), month=ExtractMonth('data_cadastro'))
            .values('year', 'month')
            .annotate(total=Count('id'))
            .order_by('year', 'month')
        )

        result = []
        for month in all_months:
            year, month = map(int, month.split('-'))
            entry = next((entry for entry in equipamentos_cadastrados if entry['year'] == year and entry['month'] == month), {'total': 0})
            result.append({
                'ano': year,
                'mes': month,
                'total': entry['total']
            })

        return Response(result)
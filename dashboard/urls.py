from django.urls import path
from .views import (
    EmpresasCadastradasNosUltimos12Meses,
    ColaboradoresCadastradosNosUltimos12Meses,
    EquipamentosCadastradosNosUltimos12Meses
)

urlpatterns = [
    # Grafico que mostra a quantidade de empresas cadastradas por mês nos ultimos 12 meses
    path('grafico_empresas_1/', EmpresasCadastradasNosUltimos12Meses.as_view(), name='empresas-cadastradas-ultimos-12-meses'),

    # Grafico que mostra a quantidade de colaboradores cadastrados por mês nos ultimos 12 meses
    path('grafico_colaboradores_1/', ColaboradoresCadastradosNosUltimos12Meses.as_view(), name='colaboradores-cadastrados-ultimos-12-meses'),

    # Grafico que mostra a quantidade de equipamentos cadastrados por mês nos ultimos 12 meses
    path('grafico_equipamentos_1/', EquipamentosCadastradosNosUltimos12Meses.as_view(), name='equipamentos-cadastrados-ultimos-12-meses'),
]

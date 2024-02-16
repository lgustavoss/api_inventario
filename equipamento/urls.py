from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipamentoViewSet, EquipamentoTransferenciaEmpresaView, EquipamentoTransferenciaColaboradorView, EquipamentoHistoricoView

#Objeto DefaultRouter para configurar as rotas automaticamente
router = DefaultRouter()
router.register(r'', EquipamentoViewSet, basename='equipamento') #'equipamento' é o nome da rota


urlpatterns = [
    path("", include(router.urls)), #incluindo as rotas geradas pelo router
    path('<int:pk>/transferencia_empresa/', EquipamentoTransferenciaEmpresaView.as_view(), name='equipamento_transferencia_empresa'),
    path('<int:pk>/transferencia_colaborador/', EquipamentoTransferenciaColaboradorView.as_view(), name='equipamento_transferencia_colaborador'),
    path('<int:pk>/atualizar_situacao/', EquipamentoViewSet.as_view({'put': 'atualizar_situacao'}), name='equipamento_atualizar_situacao'),
    path('<int:pk>/historico/', EquipamentoHistoricoView.as_view({'get': 'historico'}), name='equipamento_historico')
]

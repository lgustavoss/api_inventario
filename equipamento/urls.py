from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EquipamentoViewSet,
    EquipamentoTransferenciaEmpresaView,
    EquipamentoTransferenciaColaboradorView,
    EquipamentoHistoricoView,
    EquipamentoListSimplesViewSet,
    EquipamentoAcessoViewSet,
)


urlpatterns = [
    # GET para listar, POST para criar
    path('', EquipamentoViewSet.as_view({'get': 'list', 'post': 'create'}), name='equipamento-list'), 
    # GET para recuperar, PUT para atualizar, DELETE para excluir 
    path('<int:pk>/', EquipamentoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='equipamento-detail'),  
    path('<int:pk>/transferencia_empresa/', EquipamentoTransferenciaEmpresaView.as_view(), name='equipamento_transferencia_empresa'),
    path('<int:pk>/transferencia_colaborador/', EquipamentoTransferenciaColaboradorView.as_view(), name='equipamento_transferencia_colaborador'),
    path('<int:pk>/atualizar_situacao/', EquipamentoViewSet.as_view({'put': 'atualizar_situacao'}), name='equipamento_atualizar_situacao'),
    path('<int:pk>/historico/', EquipamentoHistoricoView.as_view({'get': 'historico'}), name='equipamento_historico'),
    path('listagem-simplificada/', EquipamentoListSimplesViewSet.as_view(), name='equipamento_listagem_simplificada'),
    path('listagem-acessos/', EquipamentoAcessoViewSet.as_view(), name='equipamento_listagem_acessos'),
]

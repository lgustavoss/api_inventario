from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipamentoViewSet, EquipamentoStatusUpdateView, EquipamentoColaboradorUpdateView, EquipamentoEmpresaUpdateView, EquipamentoSituacaoUpdateView

#Objeto DefaultRouter para configurar as rotas automaticamente
router = DefaultRouter()
router.register(r'', EquipamentoViewSet) #'equipamento' é o nome da rota


urlpatterns = [
    path("", include(router.urls)), #incluindo as rotas geradas pelo router
    path('<int:pk>/status/', EquipamentoStatusUpdateView.as_view(), name='equipamento-status-update'),
    path('<int:pk>/colaborador/', EquipamentoColaboradorUpdateView.as_view(), name='equipamento-colaborador-update'),
    path('<int:pk>/empresa/', EquipamentoEmpresaUpdateView.as_view(), name='equipamento-empresa-update'),
    path('<int:pk>/situacao/', EquipamentoSituacaoUpdateView.as_view(), name='equipamento-situacao-update'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmpresaViewSet,
    EmpresaStatusUpdateView,
    EquipamentosEmpresaView,
    EquipamentoPorTipoView,
    EquipamentoPorStatusView,
    EquipamentoPorSetorView,
    )


# Usando o DefaultRouter para configurar rotas automaticamente
router = DefaultRouter()
router.register(r'', EmpresaViewSet, basename='empresa') # 'empresa' é o nome da rota

# urls
urlpatterns = [
    # Incluindo rotas geradas pelo DefaultRouter
    path("", include(router.urls)),

    # Rota para atualizar o status de uma empresa específica por PK
    path('<int:pk>/status/', EmpresaStatusUpdateView.as_view(), name='empresa-status-update'),

    # Rota para listar os equipamentos de uma empresa especifica por PK
    path('<int:pk>/equipamentos/', EquipamentosEmpresaView.as_view(), name='empresa-equipamentos'),

    # Rota para listar a quantidade de equipamentos por tipo de equipamento
    path('<int:pk>/equipamentos-por-tipo/', EquipamentoPorTipoView.as_view(), name='equipamento-por-tipo'),

    # Rota para listar a quantidade de equipamentos por status
    path('<int:pk>/equipamentos-por-status/', EquipamentoPorStatusView.as_view(), name='equipamento-por-status'),

    # Rota para listar a quantidade de equipamentos por setor
    path('<int:pk>/equipamentos-por-setor/', EquipamentoPorSetorView.as_view(), name='equipamentos_por_setor'),
]

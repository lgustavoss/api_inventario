from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpresaViewSet, EmpresaStatusUpdateView, EmpresaTransferenciasView, EquipamentosEmpresaView


# Usando o DefaultRouter para configurar rotas automaticamente
router = DefaultRouter()
router.register(r'', EmpresaViewSet, basename='empresa') # 'empresa' é o nome da rota

# urls
urlpatterns = [
    # Incluindo rotas geradas pelo DefaultRouter
    path("", include(router.urls)),

    # Rota para atualizar o status de uma empresa específica por PK
    path('<int:pk>/status/', EmpresaStatusUpdateView.as_view(), name='empresa-status-update'),

    # Rota para listar as transferencias de equipamentos de uma empresa
    path('<int:pk>/transferencias/', EmpresaTransferenciasView.as_view(), name='empresa_transferencias'),

    # Rota para listar os equipamentos de uma empresa especifica por PK
    path('<int:pk>/equipamentos/', EquipamentosEmpresaView.as_view(), name='empresa-equipamentos')
]

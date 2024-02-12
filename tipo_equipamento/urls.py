from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TipoEquipamentoViewSet, TipoEquipamentoStatusUpdateView

#Objeto DefaultRouter para configurar as rotas automaticamente
router = DefaultRouter()
router.register(r'', TipoEquipamentoViewSet, basename='tipo_equipamento') # 'tipo_equipamento' é o nome da rota

#urls
urlpatterns = [
    # Incluindo as rotas geradas pelo router
    path("", include(router.urls)), 

    # Rotas para atualizar o status de um tipo de equipamento especifico por PK
    path('<int:pk>/status/', TipoEquipamentoStatusUpdateView.as_view(), name='tipo_equipamento-status-update')
]
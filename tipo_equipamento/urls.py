from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TipoEquipamentoViewSet

#Objeto DefaultRouter para configurar as rotas automaticamente
router = DefaultRouter()
router.register(r'', TipoEquipamentoViewSet) # 'tipo_equipamento' é o nome da rota

#urls
urlpatterns = [
    path("", include(router.urls)), #incluindo as rotas geradas pelo router
]
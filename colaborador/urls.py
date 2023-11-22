from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ColaboradorViewSet, ColaboradorStatusUpdateView

#Objeto DefaultRouter para configurar as rotas automaticamente
router = DefaultRouter()
router.register(r'', ColaboradorViewSet) # 'colaborador' é o nome da rota

#urls
urlpatterns = [
    path("", include(router.urls)), #incluindo as rotas geradas pelo router
    path('<int:pk>/status/', ColaboradorStatusUpdateView.as_view(), name='colaborador-status-update'),
]
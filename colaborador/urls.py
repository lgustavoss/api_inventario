from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ColaboradorViewSet, ColaboradorStatusUpdateView

#Objeto DefaultRouter para configurar as rotas automaticamente
router = DefaultRouter()
router.register(r'', ColaboradorViewSet) # 'colaborador' é o nome da rota

#urls
urlpatterns = [
    #incluindo as rotas geradas pelo router
    path("", include(router.urls)),

    # Rota para atualizar o status de um colaborador específico por PK
    path('<int:pk>/status/', ColaboradorStatusUpdateView.as_view(), name='colaborador-status-update'),
]
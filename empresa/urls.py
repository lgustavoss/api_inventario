from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpresaViewSet, EmpresaStatusUpdateView


#Objetivo DefaultRouter para configurar rotas automaticamente
router = DefaultRouter()
router.register(r'', EmpresaViewSet) # 'empresa' é o nome da rota

#urls
urlpatterns = [
    # Incluindo rotas geradas pelo DefaultRouter
    path("", include(router.urls)),

    # Rota para atualizar o status de uma empresa específica por PK
    path('<int:pk>/status/', EmpresaStatusUpdateView.as_view(), name='empresa-status-update'),
]

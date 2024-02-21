from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SetorViewSet, SetorStatusView, EquipamentosSetorView

# Usando o DefaultRouter para configurar rotas automaticamente
router = DefaultRouter()
router.register(r'', SetorViewSet, basename='setor') # 'setor' é o nome da rota

# urls
urlpatterns = [
    # Incluindo rotas geradas pelo DefaultRouter
    path("", include(router.urls)),

    # Rota para atualizar um status de um setor especifico por PK
    path('<int:pk>/status/', SetorStatusView.as_view(), name='setor-status-update'),

    # Rota para listar os equipamentos de um setor especifico por PK
    path('<int:pk>/equipamentos/', EquipamentosSetorView.as_view(), name='setor-equipamentos'),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SetorViewSet, SetorStatusView

# Usando o DefaultRouter para configurar rotas automaticamente
router = DefaultRouter()
router.register(r'', SetorViewSet, basename='setor') # 'setor' é o nome da rota

# urls
urlpatterns = [
    # Incluindo rotas geradas pelo DefaultRouter
    path("", include(router.urls)),
]
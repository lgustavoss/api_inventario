from django.urls import path
from users.views import (
    UserListView,
    UserDetailView,
    GrupoCreateView,
    GrupoListView,
    GrupoEditView,
    GrupoDetailView,
    AssociarUsuarioGrupo
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', UserListView.as_view(), name='user-list'), # rota para urls de usuarios
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),  # Rota para detalhes do usuário
    path('grupos/associar/', AssociarUsuarioGrupo.as_view(), name='associar-usuario-grupo'), # Rota para vincular usuarios aos grupos
    path('grupos/', GrupoListView.as_view(), name='grupo-lista'),  # Rota para listagem de grupos
    path('grupos/create/', GrupoCreateView.as_view(), name='grupo-create'), # Rota para criação de grupos
    path('grupos/editar/<int:pk>/', GrupoEditView.as_view(), name='grupo-edit'), # Rota para editar grupo
    path('grupos/<int:pk>/', GrupoDetailView.as_view(), name='grupo-detail'),  # Rota detalhada para grupos
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Rota para obtenção de tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Rota para refresh de tokens
]
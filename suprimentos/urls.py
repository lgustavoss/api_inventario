from django.urls import path, include

from .views import CategoriaViewSet


# urls
urlpatterns = [
    # GET para listar, POST para criar
    path('categorias/', CategoriaViewSet.as_view({'get': 'list', 'post': 'create'}), name='equipamento-list'), 
    # GET para recuperar, PUT para atualizar, DELETE para excluir 
    path('categorias/<int:pk>/', CategoriaViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='equipamento-detail'),  
]

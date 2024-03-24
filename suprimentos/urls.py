from django.urls import path, include

from .views import CategoriaViewSet, ItemViewSet


# urls
urlpatterns = [
    # GET para listar, POST para criar categorias
    path('categorias/', CategoriaViewSet.as_view({'get': 'list', 'post': 'create'}), name='categoria-list'), 
    # GET para recuperar, PUT para atualizar, DELETE para excluir as categorias
    path('categorias/<int:pk>/', CategoriaViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='categoria-detail'),  
    # GET para listar, POST para criar categorias
    path('item/', ItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='item-list'), 
    # GET para recuperar, PUT para atualizar, DELETE para excluir as categorias
    path('item/<int:pk>/', ItemViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='item-detail'),  
]

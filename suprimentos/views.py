from django.shortcuts import render
from .models import Categoria
from .serializers import CategoriaPaiSerialier, CategoriaFilhaSerializer
from rest_framework import viewsets, permissions

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CategoriaPaiSerialier
        return CategoriaFilhaSerializer

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Defina tipo_equipamentos como vazio se for uma categoria filha
        if not serializer.validated_data.get('tipo_equipamentos'):
            serializer.validated_data['tipo_equipamentos'] = []
        serializer.save(usuario_cadastro=self.request.user)

    def perform_update(self, serializer):
        # Defina tipo_equipamentos como vazio se for uma categoria filha
        if not serializer.validated_data.get('tipo_equipamentos'):
            serializer.validated_data['tipo_equipamentos'] = []
        serializer.save(usuario_ultima_alteracao=self.request.user)

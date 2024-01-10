from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Empresa
from .serializers import EmpresaSerializer, EmpresaStatusSerializer
from equipamento.serializers import EquipamentoSerializer
from equipamento.models import Equipamento
from users.views import has_permission_to_view_empresa, has_permission_to_detail_empresa, has_permission_to_edit_empresa


class EmpresaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manipulação de Empresas.
    """
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    pagination_class = PageNumberPagination


    def list(self, request, *args, **kwargs):
        """
        Lista todas as empresas com paginação opcional.
        """
        # Acessando o valor do 'page size' na consulta
        page_size = request.query_params.get('page_size')

        if has_permission_to_view_empresa(request.user):
            if page_size:
                #se 'page size' foi especificado, use o valor fornecido
                self.paginator.page_size = int(page_size)
            
            return super().list(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuário sem permissão para visualizar empresas'}, status=status.HTTP_403_FORBIDDEN)
        
    
    def create(self, request, *args, **kwargs):
        if has_permission_to_edit_empresa(request.user):
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Usuário sem permissão para cadastrar uma empresa'})

    def update(self, request, *args, **kwargs):
        if has_permission_to_edit_empresa(request.user):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'error': 'Usuário sem permissão para editar empresa'}, status=status.HTTP_403_FORBIDDEN)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Atualiza parcialmente uma empresa.
        """
        if has_permission_to_edit_empresa(request.user):
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuário sem permissão para editar empresas'}, status=status.HTTP_403_FORBIDDEN)
    

    def retrieve(self, request, *args, **kwargs):
        """
        Retorna os detalhes de uma empresa com os equipamentos associados.
        """
        if has_permission_to_detail_empresa(request.user):
            instance = self.get_object()
            equipamentos = Equipamento.objects.filter(empresa=instance)
            serializer = self.get_serializer(instance)
            data = serializer.data
            data['equipamentos'] = EquipamentoSerializer(equipamentos, many=True).data
            return Response(data)
        else:
            return Response({'error': 'Usuário sem permissão para visualizar os detalhes de uma empresa'}, status=status.HTTP_403_FORBIDDEN)
    

class EmpresaStatusUpdateView(APIView):
    """
    View para atualizar o status de uma empresa.
    """
    def patch(self, request, pk):
        """
        Atualiza parcialmente o status de uma empresa especificada por PK.
        """
        empresa = Empresa.objects.get(pk=pk)
        serializer = EmpresaStatusSerializer(empresa, data=request.data, partial=True)

        if has_permission_to_edit_empresa(request.user):
            serializer = EmpresaStatusSerializer(empresa, data=request.data, partial=True, context={'context': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Usuário sem permissão para alterar status de empresa'}, status=status.HTTP_403_FORBIDDEN)
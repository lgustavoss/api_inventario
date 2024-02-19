from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Empresa
from .serializers import EmpresaSerializer, EmpresaListSerializer, EmpresaStatusSerializer, EquipamentoEmpresaSerializer
from equipamento.models import Equipamento, TransferenciaEmpresa
from users.views import has_permission_to_view_empresa, has_permission_to_detail_empresa, has_permission_to_edit_empresa, has_permission_to_view_equipamento


class EmpresaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manipulação de Empresas.
    """
    def get_serializer_class(self):
        if self.action == 'list':
            return EmpresaListSerializer
        return EmpresaSerializer
    
    def get_queryset(self):
        queryset = Empresa.objects.all()
        # Filtre o queryset de acordo com as permissões do usuario
        if not has_permission_to_view_empresa(self.request.user):
            return Empresa.objects.none()
        return queryset


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
        # Retorna os detalhes de uma empresa semos equipamentos associados.
        if has_permission_to_detail_empresa(request.user):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
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
        
class EquipamentosEmpresaView(generics.ListAPIView):
    serializer_class = EquipamentoEmpresaSerializer

    def get_queryset(self):
        empresa_id = self.kwargs['pk']
        empresa = Empresa.objects.get(pk=empresa_id)

        # Verificando se o usuario tem permissao para visualizar equipamentos
        if has_permission_to_view_equipamento(self.request.user):
            queryset = empresa.equipamento_set.all()

            # Acessando o valor do page_size na consulta
            page_size = self.request.query_params.get('page_size')
            if page_size:
                self.paginator.page_size = int(page_size)
            return queryset
        else:
            return Response({'error': 'Usuário sem permissão para visualizar equipamentos'}, status=status.HTTP_403_FORBIDDEN)
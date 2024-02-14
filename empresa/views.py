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
        """
        Retorna os detalhes de uma empresa semos equipamentos associados.
        """
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
        

class EmpresaTransferenciasView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error': "Empresa não encontrada"}, status=status.HTTP_404_NOT_FOUND)

        if not has_permission_to_detail_empresa(request.user):
            return Response({'error': 'Usuário sem permissão para visualizar detalhes de uma empresa'}, status=status.HTTP_403_FORBIDDEN)
        
        # Acessando o valor do 'page size' na consulta
        page_size = request.query_params.get('page_size')
        
        # Obtendo todas as transferencias relacionadas à empresa, ordenando por data decrescente
        transferencias = TransferenciaEmpresa.objects.filter(
            Q(empresa_origem=empresa) | Q(empresa_destino=empresa)
        ).order_by('-data_transferencia')

        # Criando uma instancia de Paginator para as transferencias
        paginator = self.pagination_class()

        # Ajuste para aplicar o page_size
        if page_size:
            paginator.page_size = int(page_size)

        # Pegando o número da página a partir dos parâmetros da solicitação
        page = request.query_params.get('page', 1)

        try:
            # Obtendo a página solicitada
            transferencias_page = paginator.paginate_queryset(transferencias, request)
        except Exception as e:
            # Lidar com erros de paginação, se necessário
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Formatando informações das transferências
        transferencias_data = []

        for transferencia in transferencias_page:
            usuario_transferencia = transferencia.usuario_transferencia_empresa

            # Obtendo informações adicionais do equipamento
            equipamento = Equipamento.objects.get(pk=transferencia.equipamento.pk)
            tag_patrimonio = equipamento.tag_patrimonio
            tipo_equipamento_nome = equipamento.tipo_equipamento.tipo

            if transferencia.empresa_origem == empresa:
                outra_empresa = transferencia.empresa_destino
            else:
                outra_empresa = transferencia.empresa_origem

            transferencia_data = {
                "empresa_origem_nome": outra_empresa.nome,
                "empresa_destino_nome": empresa.nome,
                "usuario_transferencia_nome": usuario_transferencia.username,
                "data_transferencia": transferencia.data_transferencia,
                "tag_patrimonio": tag_patrimonio,
                "tipo_equipamento_nome": tipo_equipamento_nome,
            }
            transferencias_data.append(transferencia_data)

        data = {
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": transferencias_data,
        }

        return Response(data, status=status.HTTP_200_OK)

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
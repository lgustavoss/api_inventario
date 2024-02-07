from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Empresa
from .serializers import EmpresaSerializer, EmpresaStatusSerializer
from equipamento.serializers import EquipamentoSerializer, TransferenciaEmpresaSerializer
from equipamento.models import Equipamento, TransferenciaEmpresa
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
        

class EmpresaTransferenciasView(APIView):
    def get(self, request, pk):
        try:
            empresa = Empresa.objects.get(pk=pk)
        except Empresa.DoesNotExist:
            return Response({'error': "Empresa não encontrada"}, status=status.HTTP_404_NOT_FOUND)

        if not has_permission_to_detail_empresa(request.user):
            return Response({'error': 'Usuário sem permissão para visualizar detalhes de uma empresa'}, status=status.HTTP_403_FORBIDDEN)

        serializer = EmpresaSerializer(empresa)
        equipamentos = Equipamento.objects.filter(empresa=empresa)
        
        # Obtendo transferências de origem e destino, ordenando pela data de forma decrescente
        transferencias_origem = TransferenciaEmpresa.objects.filter(empresa_origem=empresa).order_by('-data_transferencia')
        transferencias_destino = TransferenciaEmpresa.objects.filter(empresa_destino=empresa).order_by('-data_transferencia')

        # Formatando informações das transferências
        transferencias_data = []

        for transferencia_origem in transferencias_origem:
            usuario_transferencia = transferencia_origem.usuario_transferencia_empresa

            # Obtendo informações adicionais do equipamento
            equipamento = Equipamento.objects.get(pk=transferencia_origem.equipamento.pk)
            tag_patrimonio = equipamento.tag_patrimonio
            tipo_equipamento_nome = equipamento.tipo_equipamento.tipo

            # Verificando se a empresa de origem é igual à empresa que estamos visualizando
            if transferencia_origem.empresa_origem == empresa:
                outra_empresa = transferencia_origem.empresa_destino
            else:
                outra_empresa = transferencia_origem.empresa_origem

            transferencia_data = {
                "empresa_origem_nome": outra_empresa.nome,
                "empresa_destino_nome": empresa.nome,
                "usuario_transferencia_nome": usuario_transferencia.username,
                "data_transferencia": transferencia_origem.data_transferencia,
                "tag_patrimonio": tag_patrimonio,
                "tipo_equipamento_nome": tipo_equipamento_nome,
            }
            transferencias_data.append(transferencia_data)

        for transferencia_destino in transferencias_destino:
            usuario_transferencia = transferencia_destino.usuario_transferencia_empresa

            # Obtendo informações adicionais do equipamento
            equipamento = Equipamento.objects.get(pk=transferencia_destino.equipamento.pk)
            tag_patrimonio = equipamento.tag_patrimonio
            tipo_equipamento_nome = equipamento.tipo_equipamento.tipo

            # Verificando se a empresa de destino é igual à empresa que estamos visualizando
            if transferencia_destino.empresa_destino == empresa:
                outra_empresa = transferencia_destino.empresa_origem
            else:
                outra_empresa = transferencia_destino.empresa_destino

            transferencia_data = {
                "empresa_origem_nome": empresa.nome,
                "empresa_destino_nome": outra_empresa.nome,
                "usuario_transferencia_nome": usuario_transferencia.username,
                "data_transferencia": transferencia_destino.data_transferencia,
                "tag_patrimonio": tag_patrimonio,
                "tipo_equipamento_nome": tipo_equipamento_nome,
            }
            transferencias_data.append(transferencia_data)

        equipamento_serializer = EquipamentoSerializer(equipamentos, many=True)

        data = {
            "empresa": serializer.data,
            "equipamentos": equipamento_serializer.data,
            "transferencias": transferencias_data,
        }

        return Response(data, status=status.HTTP_200_OK)

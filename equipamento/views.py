from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Equipamento, TransferenciaEmpresa, TransferenciaColaborador, AlteracaiSituacaoEquipamento ,SITUACAO_EQUIPAMENTO_CHOICES
from .serializers import EquipamentoSerializer, TransferenciaEmpresaSerializer, TransferenciaColaboradorSerializer, HistoricoSituacaoEquipamentoSerializer
from empresa.models import Empresa
from colaborador.models import Colaborador
from users.views import has_permission_to_view_equipamento, has_permission_to_detail_equipamento, has_permission_to_edit_equipamento


class EquipamentoViewSet(viewsets.ModelViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer
    pagination_class = PageNumberPagination

    # Listagem de todos os equipamentos
    def list(self, request, *args, **kwargs):
        #Acessando o valor do 'page size' na consulta
        page_size = request.query_params.get('page_size')

        if has_permission_to_view_equipamento(request.user):
            if page_size:
                #se 'page_size' for especificado, use o valor fornecido
                self.paginator.page_size = int(page_size)
            
            return super().list(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuário sem permissão para visualizar equipamentos'}, status=status.HTTP_403_FORBIDDEN)
    
    # Edição de um equipamento
    def update(self, request, *args, **kwargs):
        if has_permission_to_edit_equipamento(request.user):
            return super().update(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuário sem permissão para editar equipamentos'}, status=status.HTTP_403_FORBIDDEN)

    # Detalhes de um equipamento específico
    def retrieve(self, request, *args, **kwargs):
        if has_permission_to_detail_equipamento(request.user):
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            transferencias_empresa = TransferenciaEmpresa.objects.filter(equipamento=instance)
            transferencias_empresa_serializer = TransferenciaEmpresaSerializer(transferencias_empresa, many=True)
            
            transferencias_colaborador = TransferenciaColaborador.objects.filter(equipamento=instance)
            transferencias_colaborador_serializer = TransferenciaColaboradorSerializer(transferencias_colaborador, many=True)

            alteracao_situacao = AlteracaiSituacaoEquipamento.objects.filter(equipamento=instance)
            alteracao_situacao_serializer = HistoricoSituacaoEquipamentoSerializer(alteracao_situacao, many=True)

            response_data = {
                'equipamento': serializer.data,
                'transferencia_empresa': transferencias_empresa_serializer.data,
                'transferencia_colaborador': transferencias_colaborador_serializer.data,
                'alteracao_situacao': alteracao_situacao_serializer.data
            }

            return Response(response_data)
        else:
            return Response({'error': 'Usuário sem permissão para visualizar detalhes de um equipamento'}, status=status.HTTP_403_FORBIDDEN)
    
    # Atualização da situação de um equipamento
    @action(detail=True, methods=['put'])
    def atualizar_situacao(self, request, pk=None):
        if has_permission_to_edit_equipamento(request.user):
            equipamento = self.get_object()
            nova_situacao = request.data.get('situacao')

            if nova_situacao is None:
                return Response({"error":"Você deve fornecer uma nova situação para atualização."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Validando se a nova situação está entre as opções permitidas
            opcoes_situacao = dict(SITUACAO_EQUIPAMENTO_CHOICES)
            if nova_situacao not in opcoes_situacao.keys():
                return Response({"error": "Nova situação inválida."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            if nova_situacao == equipamento.situacao:
                return Response({"error": "A nova situação é igual a situação atual"}, 
                                status=status.HTTP_400_BAD_REQUEST)
            
            historico_serializer = HistoricoSituacaoEquipamentoSerializer(data={
                'equipamento': equipamento.pk,
                'situacao_anterior': equipamento.situacao,
                'situacao_nova': nova_situacao
            })

            if historico_serializer.is_valid():
                historico_serializer.save()
            else:
                return Response(historico_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            equipamento.situacao = nova_situacao
            equipamento.save()

            return Response(historico_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Usuário sem permissão para editar um equipamento'}, status=status.HTTP_403_FORBIDDEN)

    
    # Escolher o serializador apropriado
    def get_serializer_class(self):
        return EquipamentoSerializer


class EquipamentoTransferenciaEmpresaView(APIView):
    def post(self, request, pk):
        if has_permission_to_edit_equipamento(request.user):
            equipamento = Equipamento.objects.get(pk=pk)

            # Obtendo a empresa atual do equipamento
            empresa_origem_default = equipamento.empresa

            # Definindo o valor padrão para a empresa de origem na transferência
            request.data['empresa_origem'] = empresa_origem_default.id

            nova_empresa_id = request.data.get('empresa_destino')
            
            # Verificar se a empresa de origem é diferente da empresa de destino
            if nova_empresa_id == empresa_origem_default.id:
                return Response({"error": "A empresa de destino é a mesma que a empresa atual do equipamento."},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = TransferenciaEmpresaSerializer(data=request.data)
            if serializer.is_valid():
                # Salvar a transferência
                transferencia = serializer.save(equipamento=equipamento)

                # Atualizar o equipamento com a nova empresa
                nova_empresa = Empresa.objects.get(pk=nova_empresa_id)
                equipamento.empresa = nova_empresa
                equipamento.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Usuário sem permissão para editar um equipamento'}, status=status.HTTP_403_FORBIDDEN)


class EquipamentoTransferenciaColaboradorView(APIView):
    def post(self, request, pk):
        if has_permission_to_edit_equipamento(request.user):
            equipamento = Equipamento.objects.get(pk=pk)

            # Obtendo o colaborador atual do equipamento
            colaborador_origem_padrao = equipamento.colaborador

            # Definindo o valor padrão para o colaborador de origem na transferencia
            request.data['colaborador_origem'] = colaborador_origem_padrao.id

            novo_colaborador_id = request.data.get('colaborador_destino')

            # Verificando se o colaborador de origem é diferente do colaborador de destino
            if novo_colaborador_id == colaborador_origem_padrao.id:
                return Response({"error":"O colaborador e destino é o mesmo que o colaborador atual do equipamento"},
                                status=status.HTTP_400_BAD_REQUEST)
            
            serializer = TransferenciaColaboradorSerializer(data=request.data)
            if serializer.is_valid():
                # Salvar a transferencia
                transferencia = serializer.save(equipamento=equipamento)

                # Atualizando o equipamento com o novo colaborador
                novo_colaborador = Colaborador.objects.get(pk=novo_colaborador_id)
                equipamento.colaborador = novo_colaborador
                equipamento.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Usuário sem permissão para editar um equipamento'}, status=status.HTTP_403_FORBIDDEN)

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Equipamento, TransferenciaEmpresa, TransferenciaColaborador, AlteracaiSituacaoEquipamento, SITUACAO_EQUIPAMENTO_CHOICES
from .serializers import (
    EquipamentoSerializer, 
    EquipamentoListSerializer, 
    TransferenciaEmpresaSerializer, 
    TransferenciaColaboradorSerializer, 
    HistoricoSituacaoEquipamentoSerializer
)
from empresa.models import Empresa
from colaborador.models import Colaborador
from users.views import (
    has_permission_to_view_equipamento, 
    has_permission_to_detail_equipamento, 
    has_permission_to_edit_equipamento,
)


class EquipamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manipulação de Equipamentos.
    """
    def get_serializer_class(self):
        if self.action == 'list':
            return EquipamentoListSerializer
        return EquipamentoSerializer

    def get_queryset(self):
        queryset = Equipamento.objects.all()
        # Filtre o queryset de acordo com as permissoes do usuario
        if not has_permission_to_view_equipamento(self.request.user):
            return Equipamento.objects.none()
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Lista de todos os equiopamentos com paginação opcional.
        """
        #Acessando o valor do 'page size' na consulta
        page_size = request.query_params.get('page_size')

        if has_permission_to_view_equipamento(request.user):
            if page_size:
                #se 'page_size' for especificado, use o valor fornecido
                self.paginator.page_size = int(page_size)
            
            return super().list(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuário sem permissão para visualizar equipamentos'}, status=status.HTTP_403_FORBIDDEN)
        
    def create(self, request, *args, **kwargs):
        if has_permission_to_edit_equipamento(request.user):
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error':'Usuário sem permissão para criar um equipamento'}, status=status.HTTP_403_FORBIDDEN)
    
    # Edição de um equipamento
    def update(self, request, *args, **kwargs):
        if has_permission_to_edit_equipamento(request.user):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Usuário sem permissão para editar equipamentos'}, status=status.HTTP_403_FORBIDDEN)

    def atualizar_situacao(self, request, pk=None):
        if has_permission_to_edit_equipamento(request.user):
            equipamento = Equipamento.objects.get(pk=pk)
            nova_situacao = request.data.get('situacao_nova')
            
            # Verifica se a situação nova foi informada
            if nova_situacao is None:
                return Response({"error":"Você deve fornecer uma nova situação para atualização."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Verifica se a nova situação está entre as opções permitidas
            if nova_situacao not in dict(SITUACAO_EQUIPAMENTO_CHOICES).keys():
                return Response({"error": "Nova situação inválida."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Verifica se a situação nova é diferente da anterior
            if nova_situacao == equipamento.situacao:
                return Response({"error": "A nova situação é igual a situação atual"}, 
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Obtendo a situação atual do equipamento
            situacao_anterior = equipamento.situacao

            # Obtendo o usuario logado
            usuario_situacao_equipamento = request.user
            
            # Adicionando situacao_anterior e o usuario_alteracao ao payload
            request.data['situacao_anterior'] = situacao_anterior
            request.data['usuario_situacao_equipamento'] = usuario_situacao_equipamento.id

            # Criando o serializer
            serializer = HistoricoSituacaoEquipamentoSerializer(data=request.data, context={'request': request})

            if serializer.is_valid():
                # Salvando a alteracao
                alteracao = serializer.save(
                    equipamento=equipamento,
                )
                # Atualizando o equiamento com a nova situacao
                situacao_nova = nova_situacao
                equipamento.situacao = situacao_nova
                equipamento.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Usuário sem permissão para editar um equipamento'}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        # Retorna os detalhes de um equipamento sem o historico
        if has_permission_to_detail_equipamento(request.user):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'error': 'Usuario sem permissão para visualizar detalhes de um equipamento'}, status=status.HTTP_403_FORBIDDEN)

class EquipamentoTransferenciaEmpresaView(APIView):
    def post(self, request, pk):
        if has_permission_to_edit_equipamento(request.user):
            equipamento = Equipamento.objects.get(pk=pk)

            nova_empresa_id = request.data.get('empresa_destino')

            # Verificando se a empresa de origem é diferente da empresa de destino
            if nova_empresa_id == equipamento.empresa.id:
                return Response({'error': 'A empresa de destino é a mesma que a empresa atual do equipamento'},
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Obtendo a empresa de origem do equipamento
            empresa_origem = equipamento.empresa

            # Obtendo o usuario logado
            usuario_transferencia_empresa = request.user

            # Adicionando empresa_origem e usuario_transferencia_empresa ao payload
            request.data['empresa_origem'] = empresa_origem.id
            request.data['usuario_transferencia_empresa'] = usuario_transferencia_empresa.id

            # Criando o serializer
            serializer = TransferenciaEmpresaSerializer(data=request.data, context={'request': request})

            if serializer.is_valid():
                # Salvando a transferencia
                transferencia = serializer.save(
                    equipamento=equipamento,
                )

                # Atualizando o equipamento com a nova empresa
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

            novo_colaborador_id = request.data.get('colaborador_destino')

            # Verificando se o colaborador de origem é diferente do colaborador de destino
            if novo_colaborador_id == equipamento.colaborador.id:
                return Response({"error":"O colaborador e destino é o mesmo que o colaborador atual do equipamento"},
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Obtendo o colaborador de origem do equipamento
            colaborador_origem = equipamento.colaborador

            # Obtendo o usuario logado
            usuario_transferencia_colaborador = request.user

            # Adicionando o colaborador_origem e o usuario_transferencia_colaborador ao payload
            request.data['colaborador_origem'] = colaborador_origem.id
            request.data['usuario_transferencia_colaborador'] = usuario_transferencia_colaborador.id
            
            # Criando o serializer            
            serializer = TransferenciaColaboradorSerializer(data=request.data, context={'request': request})

            
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

class EquipamentoHistoricoView(EquipamentoViewSet):
    @action(detail=True, methods=['get'])
    def historico(self, request, pk=None):
        if has_permission_to_detail_equipamento(request.user):
            instance = self.get_object()

            # Criando a lista de transferencia entre empresas
            transferencias_empresa = TransferenciaEmpresa.objects.filter(equipamento=instance)
            transferencias_empresa_serializer = TransferenciaEmpresaSerializer(transferencias_empresa, many=True)

            # Criando a lista de transferencias entre colaboradores
            transferencias_colaborador = TransferenciaColaborador.objects.filter(equipamento=instance)
            transferencias_colaborador_serializer = TransferenciaColaboradorSerializer(transferencias_colaborador, many=True)

            # Criando a lista de alteração de situação
            alteracao_situacao = AlteracaiSituacaoEquipamento.objects.filter(equipamento=instance)
            alteracao_situacao_serializer = HistoricoSituacaoEquipamentoSerializer(alteracao_situacao, many=True)

            # Juntando todas as listas para montar o historico
            historico = list(
                transferencias_empresa_serializer.data +
                transferencias_colaborador_serializer.data +
                alteracao_situacao_serializer.data
            )

            # Adicionando um campo indicando o tipo de transferência
            for item in historico:
                if 'empresa_origem_nome' in item:
                    item['tipo_transferencia'] = 'Transferência entre Empresas'
                elif 'colaborador_origem_nome' in item:
                    item['tipo_transferencia'] = 'Transferência entre Colaboradores'
                else:
                    item['tipo_transferencia'] = 'Alteração de Situação'

            # Ordenando historico pela 'data_transferencia ou data_alteracao' mais recente primeiro
            historico_ordenado = sorted(historico, key=lambda x: x.get('data_transferencia', x.get('data_alteracao')), reverse=True)

            response_data = {
                'historico': historico_ordenado,
            }

            return Response(response_data)
        else:
            return Response({'error': 'Usuario sem permissão para visualizar os detalhes de um equipamento'}, status=status.HTTP_403_FORBIDDEN)

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Equipamento, TransferenciaEmpresa, TransferenciaColaborador
from .serializers import EquipamentoSerializer, TransferenciaEmpresaSerializer, TransferenciaColaboradorSerializer
from empresa.models import Empresa



class EquipamentoViewSet(viewsets.ModelViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer
    pagination_class = PageNumberPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == 'list':
            context['include_transferencias'] = True
        return context

    def list(self, request, *args, **kwargs):
        #Acessando o valor do 'page size' na consulta
        page_size = request.query_params.get('page_size')

        if page_size:
            #se 'page_size' for especificado, use o valor fornecido
            self.paginator.page_size = int(page_size)
        
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        transferencias_empresa = TransferenciaEmpresa.objects.filter(equipamento=instance)
        transferencias_empresa_serializer = TransferenciaEmpresaSerializer(transferencias_empresa, many=True)
        
        transferencias_colaborador = TransferenciaColaborador.objects.filter(equipamento=instance)
        transferencias_colaborador_serializer = TransferenciaColaboradorSerializer(transferencias_colaborador, many=True)

        response_data = {
            'equipamento': serializer.data,
            'transferencia_empresa': transferencias_empresa_serializer.data,
            'transferencia_colaborador': transferencias_colaborador_serializer.data
        }

        return Response(response_data)


class EquipamentoTransferenciaEmpresaView(APIView):
    def post(self, request, pk):
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



class EquipamentoTransferenciaColaboradorView(APIView):
    def post(self, request, pk):
        equipamento = Equipamento.objects.get(pk=pk)

        serializer = TransferenciaColaboradorSerializer(data=request.data)
        if serializer.is_valid():
            # Incluir o equipamento no serializer antes de salvar
            serializer.validated_data['equipamento'] = equipamento
            transferencia = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
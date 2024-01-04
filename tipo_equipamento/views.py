from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .serializers import TipoEquipamentoSerializer
from .models import TipoEquipamento
from equipamento.serializers import EquipamentoSerializer
from equipamento.models import Equipamento
from users.views import has_permission_to_view_tipo_equipamento, has_permission_to_detail_tipo_equipamento, has_permission_to_edit_tipo_equipamento


class TipoEquipamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manipulação dos tipos de equipamentos
    """
    queryset = TipoEquipamento.objects.all()
    serializer_class = TipoEquipamentoSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        """
        Lista todos os tipode de equipamentos com paginação opcional.
        """
        #Acessando o valor do 'page size' na consulta
        page_size = request.query_params.get('page_size')

        if has_permission_to_view_tipo_equipamento(request.user):
            if page_size:
                #se 'page_size' for especificado, use o valor fornecido
                self.paginator.page_size = int(page_size)

            return super().list(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuário sem permissão para visualizar tipos de equipamento'}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if has_permission_to_edit_tipo_equipamento(request.user):
            return super().update(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuário sem permissão para editar tipos de equipamento'}, status=status.HTTP_403_FORBIDDEN)

    
    def partial_update(self, request, *args, **kwargs):
        """
        Atualiza parcialmente um tipo de equipamento.
        """
        if has_permission_to_edit_tipo_equipamento(request.user):
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuário sem permissão para editar tipos de equipamento'}, status=status.HTTP_403_FORBIDDEN)


    def retrieve(self, request, *args, **kwargs):
        """
        Retorna os tipos de equipamentos com os equipamentos associados.
        """
        if has_permission_to_detail_tipo_equipamento(request.user):
            instance = self.get_object()
            equipamentos = Equipamento.objects.filter(tipo_equipamento=instance)
            serializer = self.get_serializer(instance)
            data = serializer.data
            data['equipamentos'] = EquipamentoSerializer(equipamentos, many=True).data
            return Response(data)
        else:
            return Response({'error': 'Usuário sem permissão para visualizar detalhes dos tipos de equipamento'}, status=status.HTTP_403_FORBIDDEN)

    
class TipoEquipamentoStatusUpdateView(APIView):
    """
    View para atualizar o status de um tipo de equipamento.
    """
    def patch(self, request, pk):
        """
        Atualiza parcialmente o status de um tipod e equipamento especificado por PK.
        """
        tipo_equipamento = TipoEquipamento.objects.get(pk=pk)
        serializer = TipoEquipamentoSerializer(tipo_equipamento, data=request.data, partial=True)

        if has_permission_to_edit_tipo_equipamento(request.user):
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Usuário sem permissão para alterar o status do tipo de equipamento'}, status=status.HTTP_403_FORBIDDEN)

    

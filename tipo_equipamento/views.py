from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TipoEquipamentoSerializer, TipoEquipamentoListSerializer, EquipamentoTipoEquipamentoSerializer
from .models import TipoEquipamento
from users.views import (
    has_permission_to_view_tipo_equipamento,
    has_permission_to_detail_tipo_equipamento,
    has_permission_to_edit_tipo_equipamento, 
    has_permission_to_view_equipamento
)


class TipoEquipamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manipulação dos tipos de equipamentos
    """
    def get_serializer_class(self):
        if self.action == 'list':
            return TipoEquipamentoListSerializer
        return TipoEquipamentoSerializer
    
    def get_queryset(self):
        queryset = TipoEquipamento.objects.all()
        # Filtre o queryset de acordo com as permissões do usuario
        if not has_permission_to_view_tipo_equipamento(self.request.user):
            return TipoEquipamento.objects.none()
        return queryset

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
        
    def create(self, request, *args, **kwargs):
        if has_permission_to_edit_tipo_equipamento(request.user):
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error':'Usuario sem permissão para criar um tipo de equipamento'}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if has_permission_to_edit_tipo_equipamento(request.user):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
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
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
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

        if has_permission_to_edit_tipo_equipamento(request.user):
            serializer = TipoEquipamentoSerializer(tipo_equipamento, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Usuário sem permissão para alterar o status do tipo de equipamento'}, status=status.HTTP_403_FORBIDDEN)

class EquipamentoTipoEquipamentoView(generics.ListAPIView):
    serializer_class = EquipamentoTipoEquipamentoSerializer

    def get_queryset(self):
        tipo_equipamento_id = self.kwargs['pk']
        tipo_equipamento = TipoEquipamento.objects.get(pk=tipo_equipamento_id)

        # Verificando se o usuario tem permissão para visualizar os equipamentos
        if has_permission_to_view_equipamento(self.request.user):
            queryset = tipo_equipamento.equipamento_set.all()

            # Acessando o valor do page_size na consulta
            page_size = self.request.query_params.get('page_size')
            if page_size:
                self.paginator.page_size = int(page_size)
            return queryset
        else:
            return Response({'error': 'Usuário sem permissão para visualizar equipamentos'}, status=status.HTTP_403_FORBIDDEN)
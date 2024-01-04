from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Colaborador
from .serializers import ColaboradorSerializer, ColaboradorStatusSerializer
from equipamento.serializers import EquipamentoSerializer
from equipamento.models import Equipamento
from users.views import has_permission_to_view_colaborador, has_permission_to_detail_colaborador, has_permission_to_edit_colaborador


# 
class ColaboradorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manipulação de Colaboradores.
    """
    queryset = Colaborador.objects.all()
    serializer_class = ColaboradorSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        """
        Lista de todos os colaboradores com paginação opcional.
        """
        #Acessando o valor do 'page size' na consulta
        page_size = request.query_params.get('page_size')
        
        if has_permission_to_view_colaborador(request.user):
            if page_size:
                #se 'page_size' for especificado, use o valor fornecido
                self.paginator.page_size = int(page_size)
            
            return super().list(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuário sem permissão para visualizar colaboradores'}, status=status.HTTP_403_FORBIDDEN)
    
    def update(self, request, *args, **kwargs):
        if has_permission_to_edit_colaborador(request.user):
            return super().update(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuário sem permissão para editar colaborador'}, status=status.HTTP_403_FORBIDDEN)


    def partial_update(self, request, *args, **kwargs):
        """
        Atualiza parcialmente um colaborador.
        """
        if has_permission_to_edit_colaborador(request.user):
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuário sem permissão para editar colaborador'}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        """
        Retorna os detalhes de um colaborador com os equipamentos associados.
        """
        if has_permission_to_detail_colaborador(request.user):
            instance = self.get_object()
            equipamentos = Equipamento.objects.filter(colaborador=instance)
            serializer = self.get_serializer(instance)
            data = serializer.data
            data['equipamentos'] = EquipamentoSerializer(equipamentos, many=True).data
            return Response(data)
        else:
            return Response({'error': 'Usuário sem permissão para editar colaborador'}, status=status.HTTP_403_FORBIDDEN)



class ColaboradorStatusUpdateView(APIView):
    """
    View para atualizar o status de um colaborador.
    """
    def patch(self, request, pk):
        """
        Atualiza parcialmente o status de um colaborador especificado por PK.
        """
        colaborador = Colaborador.objects.get(pk=pk)
        serializer = ColaboradorStatusSerializer(colaborador, data=request.data, partial=True)

        if has_permission_to_edit_colaborador(request.user):
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Usuário sem permissão para editar colaborador'}, status=status.HTTP_403_FORBIDDEN)

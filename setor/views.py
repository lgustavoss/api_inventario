from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SetorListSerializer, SetorSerializer, SetorStatusSerializer, EquipamentoSetorSerializer
from .models import Setor
from users.views import has_permission_to_detail_setor, has_permission_to_edit_setor, has_permission_to_view_setor, has_permission_to_view_equipamento


class SetorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manipulação dos Setores
    """
    def get_serializer_class(self):
        if self.action == 'list':
            return SetorListSerializer
        return SetorSerializer
    
    def get_queryset(self):
        queryset = Setor.objects.all()
        # Filtre de acordo com as permissões do usuario
        if not has_permission_to_view_setor(self.request.user):
            return Setor.objects.none()
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        Lista todos os setores com paginacao opcional
        """
        # Acessando o valor do 'page_size' na consulta
        page_size = request.query_params.get('page_size')

        if has_permission_to_view_setor(request.user):
            if page_size:
                # Se 'page_size' foi especificado, use o valor fornecido
                self.paginator.page_size = int(page_size)
            
            return super().list(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuario sem permissão para visualizar setores'}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        if has_permission_to_edit_setor(request.user):
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Usuario sem permissão para editar um setor'})
        
    def partial_update(self, request, *args, **kwargs):
        """
        Atualiza parcialmente um setor
        """
        if has_permission_to_edit_setor(request.user):
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuario sem permissão para editar um setor'})
        
    
    def retrieve(self, request, *args, **kwargs):
        # Retorna os detalhes de uma setor sem as empresas associadas.
        if has_permission_to_detail_setor(request.user):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'error': 'Usuário sem permissão para visualizar os detalhes de uma setor'}, status=status.HTTP_403_FORBIDDEN)

class SetorStatusView(APIView):
    """
    View para atualizar o status de um setor.
    """
    def patch(self, request, pk):
        """
        Atualiza parcialmente o status de uma status especificada por PK.
        """
        setor = Setor.objects.get(pk=pk)
        serializer = SetorStatusSerializer(setor, data=request.data, partial=True)

        if has_permission_to_edit_setor(request.user):
            serializer = SetorStatusSerializer(setor, data=request.data, partial=True, context={'context': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Usuário sem permissão para alterar status de um setor'}, status=status.HTTP_403_FORBIDDEN)
        
class EquipamentosSetorView(APIView):
    serializer_class = EquipamentoSetorSerializer

    def get(self, request, *args, **kwargs):
        setor_id = self.kwargs['pk']
        setor = Setor.objects.get(pk=setor_id)

        # Verificando se o usuario tem permissão para visualizar equipamentos
        if has_permission_to_view_equipamento(self.request.user):
            queryset = setor.equipamento_set.all()

            # Acessando o valor do page_size na consulta
            page_size = self.request.query_params.get('page_size')
            if page_size:
                self.paginator.page_size = int(page_size)
            
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'Usuário sem permissão para visualizar equipamentos'}, status=status.HTTP_403_FORBIDDEN)
    
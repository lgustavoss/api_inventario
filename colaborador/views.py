from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Colaborador
from .serializers import ColaboradorSerializer, ColaboradorStatusSerializer, ColaboradorListSerializer, EquipamentoColaboradorSerializer
from users.views import has_permission_to_view_colaborador, has_permission_to_detail_colaborador, has_permission_to_edit_colaborador, has_permission_to_view_equipamento



class ColaboradorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manipulação de Colaboradores.
    """
    def get_serializer_class(self):
        if self.action == 'list':
            return ColaboradorListSerializer
        return ColaboradorSerializer
    
    def get_queryset(self):
        queryset = Colaborador.objects.all()
        # Filtre o queryset de acordo com as permissões do usuario
        if not has_permission_to_view_colaborador(self.request.user):
            return Colaborador.objects.none()
        return queryset

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
    
    def create(self, request, *args, **kwargs):
        if has_permission_to_edit_colaborador(request.user):
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Usuário sem permissão para criar colaborador'}, status=status.HTTP_403_FORBIDDEN)
    
    def update(self, request, *args, **kwargs):
        if has_permission_to_edit_colaborador(request.user):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
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
        Retorna os detalhes de um colaborador sem os equipamentos associados.
        """
        if has_permission_to_detail_colaborador(request.user):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'error': 'Usuário sem permissão visualizar detalhes do colaborador'}, status=status.HTTP_403_FORBIDDEN)



class ColaboradorStatusUpdateView(APIView):
    """
    View para atualizar o status de um colaborador.
    """
    def patch(self, request, pk):
        """
        Atualiza parcialmente o status de um colaborador especificado por PK.
        """
        colaborador = Colaborador.objects.get(pk=pk)

        if has_permission_to_edit_colaborador(request.user):
            serializer = ColaboradorStatusSerializer(colaborador, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Usuário sem permissão para editar colaborador'}, status=status.HTTP_403_FORBIDDEN)
        

class EquipamentosColaboradorView(generics.ListAPIView):
    serializer_class = EquipamentoColaboradorSerializer

    def get_queryset(self):
        colaborador_id = self.kwargs['pk']
        queryset = Colaborador.objects.get(pk=colaborador_id).equipamento_set.all()

        # Acessando o valor do page_size na consulta
        page_size = self.request.query_params.get('page_size')
        if page_size:
            self.paginator.page_size = int(page_size)
        
        return queryset

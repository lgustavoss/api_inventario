from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import CategoriaSerializer, CategoriaListSerializer
from .models import Categoria
from users.views import has_permission_to_detail_categoria, has_permission_to_edit_categoria, has_permission_to_view_categoria



class CategoriaViewSet(viewsets.ModelViewSet):
    """
    Viewset para manipulação de Categorias
    """
    def get_serializer_class(self):
        if self.action == 'list':
            return CategoriaListSerializer
        return CategoriaSerializer
    
    def get_queryset(self):
        queryset = Categoria.objects.all()
        # Filtre de acordo com as permissões do usuário
        if not has_permission_to_view_categoria(self.request.user):
            return Categoria.objects.none()
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        Lista de todas as categorias com paginacao opcional
        """
        # Acessando o valor do 'page size' na consulta
        page_size = request.query_params.get('page_size')

        if has_permission_to_view_categoria(request.user):
            if page_size:
                # Se 'page_size' for especificado, use o valor fornecido
                self.paginator.page_size = int(page_size)
            return super().list(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuário sem permissão para visualizar categorias'}, status=status.HTTP_403_FORBIDDEN)
            
    def create(self, request, *args, **kwargs):
        user = request.user
        if has_permission_to_edit_categoria(user):
            # Certifique-se de que o campo tipo_equipamento esteja presente nos dados da solicitação
            if 'tipo_equipamento' not in request.data:
                return Response({'error': 'O campo tipo_equipamento é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

            # Copie e trate os dados da solicitação
            data = request.data.copy()
            data['usuario_cadastro'] = user.id
            
            tipo_equipamento_ids = data.pop('tipo_equipamento')  # Remova e armazene os IDs do tipo de equipamento

            # Remova temporariamente o campo tipo_equipamento do serializer durante a criação
            class CustomSerializer(self.get_serializer_class()):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.fields['tipo_equipamento'].required = False

            serializer = CustomSerializer(data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)

            # Antes de salvar a instância, crie-a para poder adicionar os tipos de equipamento
            instance = serializer.save()

            # Adicione os tipos de equipamento à instância criada
            instance.tipo_equipamento.set(tipo_equipamento_ids)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Usuário sem permissão para criar uma categoria'}, status=status.HTTP_403_FORBIDDEN)


    def update(self, request, *args, **kwargs):
        if has_permission_to_edit_categoria(request.user):
            instance = self.get_object()

            # Extrai os IDs do tipo de equipamento, se estiverem presentes
            tipo_equipamento_ids = request.data.pop('tipo_equipamento', [])

            # Adicione 'usuario_cadastro' aos dados enviados para o serializer
            request.data['usuario_cadastro'] = request.user.id

            # Remova temporariamente a obrigatoriedade do campo tipo_equipamento
            class CustomSerializer(self.get_serializer_class()):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self.fields['tipo_equipamento'].required = False

            serializer = CustomSerializer(instance, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Atualize os tipos de equipamento da instância apenas se houver IDs de tipo de equipamento
            if tipo_equipamento_ids:
                instance.tipo_equipamento.set(tipo_equipamento_ids)
            else:
                instance.tipo_equipamento.clear()  # Limpa os tipos de equipamento, se não houver IDs fornecidos

            return Response(serializer.data)
        else:
            return Response({'error': 'Usuário sem permissão para editar uma categoria'}, status=status.HTTP_403_FORBIDDEN)


    def partial_update(self, request, *args, **kwargs):
        # Atualiza parcialmente uma categoria
        if has_permission_to_edit_categoria(request.user):
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        else:
            return Response({'error': 'Usuário sem permissão para editar uma categoria'}, status=status.HTTP_403_FORBIDDEN)
        
    def retrieve(self, request, *args, **kwargs):
        """
        Retorna os dados de uma categoria sem os itens associados
        """
        if has_permission_to_detail_categoria(request.user):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({'error': "Usuário sem permissão para visualizar os detalhes da categoria"})
        
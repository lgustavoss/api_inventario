from django.contrib.auth.models import User, Group, Permission
from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import UserSerializer, GrupoSerializer, GrupoDetailSerializer


class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GrupoCreateView(APIView):
    def post(self, request, format=None):
        grupo_nome = request.data.get('name')
        permissoes_grupo = request.data.get('permissions') # Recebe as permissões do payload

        if Group.objects.filter(name=grupo_nome).exists():
            return Response({'error': 'O grupo já existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        grupo = Group(name=grupo_nome)
        grupo.save()

        if permissoes_grupo:
            for permissao_nome, valor in permissoes_grupo.items():
                try:
                    permissao = Permission.objects.get(codename=permissao_nome)
                    if valor:
                        grupo.permissions.add(permissao)
                    else:
                        grupo.permissions.remove(permissao)
                except Permission.DoesNotExist:
                    return Response(f'A permissão {permissao_nome} não existe', status=status.HTTP_404_NOT_FOUND)

        # Obtem todas as permissões do grupo
        permissao_lista = [str(permission) for permission in grupo.permissions.all()]

        data = {
            'sucesso': 'Grupo criado com sucesso',
            'name': grupo_nome,
            'permissoes': permissao_lista
        }

        return Response(data, status=status.HTTP_201_CREATED)
    
class GrupoListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GrupoSerializer

class GrupoDetailView(RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GrupoDetailSerializer

class GrupoEditView(APIView):
    def get_grupo(self, pk):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return None

    def put(self, request, pk, format=None):
        grupo = self.get_grupo(pk)
        if not grupo:
            return Response({'error': 'Grupo não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        novo_nome = request.data.get('name')
        novas_permissoes = request.data.get('permissions')  # Recebe as permissões do payload

        if novo_nome:
            grupo.name = novo_nome
            grupo.save()

        if novas_permissoes is not None:
            grupo.permissions.clear()  # Remove todas as permissões associadas ao grupo
            for permissao_nome, valor in novas_permissoes.items():
                try:
                    permissao = Permission.objects.get(codename=permissao_nome)
                    if valor:
                        grupo.permissions.add(permissao)
                except Permission.DoesNotExist:
                    return Response(f'A permissão {permissao_nome} não existe', status=status.HTTP_404_NOT_FOUND)

        serializer = GrupoSerializer(grupo)
        return Response(serializer.data)


class AssociarUsuarioGrupo(APIView):
    def post(self, request, format=None):
        user_id = request.data.get('user_id')
        grupos_ids = request.data.get('groups', [])  # Recebe a lista de IDs dos grupos do payload

        try:
            usuario = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Remover todos os grupos atuais do usuário
        usuario.groups.clear()

        # Adiciondo os novos grupos ao usuário
        for grupo_id in grupos_ids:
            try:
                grupo = Group.objects.get(pk=grupo_id)
                usuario.groups.add(grupo)
            except Group.DoesNotExist:
                return Response({'error': f'O grupo com ID {grupo_id} não existe'}, status=status.HTTP_404_NOT_FOUND)

        # Agora, vamos buscar novamente o usuário para retornar seus detalhes atualizados
        usuario = User.objects.prefetch_related('groups').get(pk=user_id)
        serializer = UserSerializer(usuario)

        return Response(serializer.data, status=status.HTTP_200_OK)


def has_permission_to_view_empresa(user):
    # Verificar se o usuário está associado a grupos que tenham a permissão adequada
    grupos_com_permissao = Group.objects.filter(permissions__codename='visualizar_empresa', user=user)
    
    # Se houver algum grupo com permissão, o usuário pode visualizar empresas
    return grupos_com_permissao.exists()


def has_permission_to_detail_empresa(user):
    # Verificar se o usuário está associado a grupos que tenham a permissão adequada
    grupos_com_permissao = Group.objects.filter(permissions__codename='visualiza_detalhe_empresa', user=user)
    
    # Se houver algum grupo com permissão, o usuário pode visualizar detalhes de uma empresa
    return grupos_com_permissao.exists()

def has_permission_to_edit_empresa(user):
    # Verificar se o usuário está associado a grupos que tenham a permissão adequada
    grupos_com_permissao = Group.objects.filter(permissions__codename='editar_empresa', user=user)
    
    # Se houver algum grupo com permissão, o usuário pode editar uma empresa
    return grupos_com_permissao.exists()

def has_permission_to_view_colaborador(user):
    # Verificar se o usuário está associado a grupos que tenham a permissão adequada
    grupos_com_permissao = Group.objects.filter(permissions__codename='visualizar_colaborador', user=user)

    # Se houver algum grupo com permisão, o usuário pode visualizar colaborador
    return grupos_com_permissao.exists()

def has_permission_to_detail_colaborador(user):
    # Verificar se o usuário está associado a grupos que tenham a permissão adequada
    grupos_com_permissao = Group.objects.filter(permissions__codename='visualiza_detalhe_colaborador', user=user)
    
    # Se houver algum grupo com permissão, o usuário pode visualizar detalhes de uma colaborador
    return grupos_com_permissao.exists()

def has_permission_to_edit_colaborador(user):
    # Verificar se o usuário está associado a grupos que tenham a permissão adequada
    grupos_com_permissao = Group.objects.filter(permissions__codename='editar_colaborador', user=user)
    
    # Se houver algum grupo com permissão, o usuário pode editar uma colaborador
    return grupos_com_permissao.exists()

def has_permission_to_view_tipo_equipamento(user):
    # Verificar se o usuário está associado a grupos que tenham a permissão adequada
    grupos_com_permissao = Group.objects.filter(permissions__codename='visualizar_tipo_equipamento', user=user)

    # Se houver algum grupo com permisão, o usuário pode visualizar tipo_equipamento
    return grupos_com_permissao.exists()

def has_permission_to_detail_tipo_equipamento(user):
    # Verificar se o usuário está associado a grupos que tenham a permissão adequada
    grupos_com_permissao = Group.objects.filter(permissions__codename='visualiza_detalhe_tipo_equipamento', user=user)
    
    # Se houver algum grupo com permissão, o usuário pode visualizar detalhes de uma tipo_equipamento
    return grupos_com_permissao.exists()

def has_permission_to_edit_tipo_equipamento(user):
    # Verificar se o usuário está associado a grupos que tenham a permissão adequada
    grupos_com_permissao = Group.objects.filter(permissions__codename='editar_tipo_equipamento', user=user)
    
    # Se houver algum grupo com permissão, o usuário pode editar uma tipo_equipamento
    return grupos_com_permissao.exists()


def has_permission_to_view_equipamento(user):
    # Verificar se o usuário está associado a grupos que tenham a permissão adequada
    grupos_com_permissao = Group.objects.filter(permissions__codename='visualizar_equipamento', user=user)

    # Se houver algum grupo com permisão, o usuário pode visualizar equipamento
    return grupos_com_permissao.exists()

def has_permission_to_detail_equipamento(user):
    # Verificar se o usuário está associado a grupos que tenham a permissão adequada
    grupos_com_permissao = Group.objects.filter(permissions__codename='visualiza_detalhe_equipamento', user=user)
    
    # Se houver algum grupo com permissão, o usuário pode visualizar detalhes de uma equipamento
    return grupos_com_permissao.exists()

def has_permission_to_edit_equipamento(user):
    # Verificar se o usuário está associado a grupos que tenham a permissão adequada
    grupos_com_permissao = Group.objects.filter(permissions__codename='editar_equipamento', user=user)
    
    # Se houver algum grupo com permissão, o usuário pode editar uma equipamento
    return grupos_com_permissao.exists()

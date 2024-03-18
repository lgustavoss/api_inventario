from django.db import models
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType


class Setor(models.Model):
    """
    Modelo para representar os setores das empresas
    """
    # Nome do setor
    nome = models.CharField(max_length=100, null=False, blank=False)

    # Status do setor, indicando se está ativo ou não (padrão: ativo)
    status = models.BooleanField(default=True)

    # Data de cadastro da setor(auto_now_add garante que é preenchido automaticamente na criação)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    # Usuário que cadastrou a setor(relacionamento ForeignKey com o modelo user do Django)
    usuario_cadastro = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='setores_criadas', null=True)

    # Data da ultima ateração da setor
    data_ultima_alteracao = models.DateTimeField(null=True, default=None)

    # Usuário que realizou a ultima alteração na setor
    usuario_ultima_alteracao = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='setores_alteradas', null=True)

    class Meta:
        # Ordenando as setors pelo nome por padrão
        ordering = ['id']


# Método para criar as permissões após as migrações
def create_permissions(sender, **kwargs):
    if sender.name == 'setor':
        content_type = ContentType.objects.get_for_model(Setor)

        visualizar_setor, created = Permission.objects.get_or_create(
            codename='visualizar_setor',
            name='Visualizar setores',
            content_type=content_type,
        )

        visualiza_detalhe_setor, created = Permission.objects.get_or_create(
            codename='visualiza_detalhe_setor',
            name='Visualizar Detalhes do setor',
            content_type=content_type,
        )

        editar_setor, created = Permission.objects.get_or_create(
            codename='editar_setor',
            name='Editar setor',
            content_type=content_type,
        )

# Conectar o método ao sinal post_migrate
post_migrate.connect(create_permissions)
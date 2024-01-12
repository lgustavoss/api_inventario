from django.db import models
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType

# Criando models do Tipo de Equipamento


class TipoEquipamento(models.Model):
    """
    Modelo para representar os tipos de equipamento.
    """
    tipo = models.CharField(max_length=100, null=False, blank=False)

    # Status para indicar se o tipo está ativo (padrão: ativo)
    status = models.BooleanField(default=True)

    # Data de cadastro do tipo de equipamento (auto now garante que é preenchido automaticamente na criação)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    # Usuário que cadastrou o tipo de equipamento (relacionamento ForeignKey com o modelo User do Django)
    usuario_cadastro = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='tipo_equipamentos_criados', null=True)

    # Data da ultima alteração do tipo de equipamento
    data_ultima_alteracao = models.DateTimeField(null=True, default=None)

    # Usuario da ultima alteração no tipo de equipamento
    usuario_ultima_alteracao = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='tipo_equipamento_alterados', null=True)

    class Meta:
        ordering = ['tipo']


# Método para criar as permissões após as migrações
def create_permissions(sender, **kwargs):
    if sender.name == 'tipo_equipamento':
        content_type = ContentType.objects.get_for_model(TipoEquipamento)

        visualizar_tipo_equipamento, created = Permission.objects.get_or_create(
            codename='visualizar_tipo_equipamento',
            name='Visualizar Tipos de Equipamentos',
            content_type=content_type,
        )

        visualiza_detalhe_tipo_equipamento, created = Permission.objects.get_or_create(
            codename='visualiza_detalhe_tipo_equipamento',
            name='Visualizar Detalhes do Tipo de Equipamento',
            content_type=content_type,
        )

        editar_tipo_equipamento, created = Permission.objects.get_or_create(
            codename='editar_tipo_equipamento',
            name='Editar Tipo de Equipamento',
            content_type=content_type,
        )

# Conectar o método ao sinal post_migrate
post_migrate.connect(create_permissions)
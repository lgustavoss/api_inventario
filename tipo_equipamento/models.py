from django.db import models
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class TipoEquipamento(models.Model):
    """
    Modelo para representar os tipos de equipamento.
    """
    tipo = models.CharField(max_length=100, null=False, blank=False)

    # Status para indicar se o tipo está ativo (padrão: ativo)
    status = models.BooleanField(default=True)

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
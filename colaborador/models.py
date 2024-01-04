from django.db import models
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .validators import validar_cpf


class Colaborador(models.Model):
    """
    Modelo para representar os colaboradores
    """
    # Nome do colaborador
    nome = models.CharField(max_length=100, null=False, blank=False)

    # CPF do colaborador, único e validado pelo validador validar_cpf
    cpf = models.CharField(max_length=14, null=False, blank=False, unique=True, validators=[validar_cpf])

    # Status do colaborador, indicando se está ativo ou não (padrão: ativo)
    status = models.BooleanField(default=True)

    class Meta:
        # Ordenando os colaboradores pelo nome por padrão
        ordering = ['nome']


# Método para criar as permissões após as migrações
def create_permissions(sender, **kwargs):
    if sender.name == 'colaborador':
        content_type = ContentType.objects.get_for_model(Colaborador)

        visualizar_colaborador, created = Permission.objects.get_or_create(
            codename = 'visualizar_colaborador',
            name = 'Visualizar Colaboradores',
            content_type = content_type,
        )

        visualiza_detalhe_colaborador, created = Permission.objects.get_or_create(
            codename = 'visualiza_detalhe_colaborador',
            name = 'Visualiar Detalhes do Colaborador',
            content_type = content_type,
        )

        editar_colaborador, created = Permission.objects.get_or_create(
            codename = 'editar_colaborador',
            name = 'Editar Colaborador',
            content_type = content_type,
        )

# Concectar o método ao sinal post_mnigrate
post_migrate.connect(create_permissions)
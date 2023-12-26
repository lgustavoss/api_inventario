from django.db import models
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .validators import validar_cnpj


class Empresa(models.Model):
    """
    Modelo para representar as empresas
    """
    # Campos do modelo Empresa
    nome = models.CharField(max_length=100, null=False, blank=False)
    cnpj = models.CharField(max_length=18, null=False, blank=False, unique=True, validators=[validar_cnpj])
    status = models.BooleanField(default=True)

    class Meta:
        # Ordenando as empresas pelo nome por padrão
        ordering = ['nome']
    
    pass

# Método para criar as permissões após as migrações
def create_permissions(sender, **kwargs):
    if sender.name == 'empresa':
        content_type = ContentType.objects.get_for_model(Empresa)

        visualizar_empresa, created = Permission.objects.get_or_create(
            codename='visualizar_empresa',
            name='Visualizar empresas',
            content_type=content_type,
        )

        visualiza_detalhe_empresa, created = Permission.objects.get_or_create(
            codename='visualiza_detalhe_empresa',
            name='Visualizar Detalhes da Empresa',
            content_type=content_type,
        )

        editar_empresa, created = Permission.objects.get_or_create(
            codename='editar_empresa',
            name='Editar Empresa',
            content_type=content_type,
        )

# Conectar o método ao sinal post_migrate
post_migrate.connect(create_permissions)
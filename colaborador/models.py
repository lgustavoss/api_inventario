from django.db import models
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Permission, User
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

    # Data de cadastro do colaborador (auto_now_add garante que é preenchido automaticamente na criação)
    data_cadastro = models.DateTimeField(auto_now_add = True)

    # Usuário que cadastrou o colaborador (relacionamento ForeignKey com o modelo user do Django)
    usuario_cadastro = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='colaboradores_criados', null=True)

    # Data da ultima alteração do colaborador
    data_ultima_alteracao = models.DateTimeField(null=True, default=None)

    # Usuário que realizou a ultima alteração no colaborador
    usuario_ultima_alteracao = models.ForeignKey(User, on_delete = models.SET_NULL, related_name='colaboradores_alterados', null=True)

    class Meta:
        # Ordenando os colaboradores pelo id por padrão
        ordering = ['id']


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
            name = 'Visualizar Detalhes do Colaborador',
            content_type = content_type,
        )

        editar_colaborador, created = Permission.objects.get_or_create(
            codename = 'editar_colaborador',
            name = 'Editar Colaborador',
            content_type = content_type,
        )

# Concectar o método ao sinal post_mnigrate
post_migrate.connect(create_permissions)
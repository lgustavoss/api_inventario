from django.db import models
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from empresa.models import Empresa
from colaborador.models import Colaborador
from tipo_equipamento.models import TipoEquipamento
from setor.models import Setor

# Choices para situação de equipamento
SITUACAO_EQUIPAMENTO_CHOICES = (
    ('0', 'Novo'),
    ('1', 'Em operação'),
    ('2', 'Em manutenção'),
    ('3', 'Disponivel'),
    ('4', 'Indisponível'),
)

class Equipamento(models.Model):
    tag_patrimonio = models.CharField(
        max_length=30, null=False, blank=False, unique=True)
    tipo_equipamento = models.ForeignKey(
        TipoEquipamento, on_delete=models.PROTECT, limit_choices_to={'status': True})
    pedido = models.CharField(
        max_length=20, null=True, blank=True, editable=True)
    data_compra = models.DateField(
        blank=True, null=True, editable=True)
    situacao = models.CharField(
        max_length=1, choices=SITUACAO_EQUIPAMENTO_CHOICES, null=False, blank=False)
    empresa = models.ForeignKey(
        Empresa, on_delete=models.PROTECT, limit_choices_to={'status': True})
    colaborador = models.ForeignKey(
        Colaborador, on_delete=models.PROTECT, limit_choices_to={'status': True})
    setor = models.ForeignKey(
        Setor, on_delete=models.PROTECT, limit_choices_to={'status': True}, blank=True, null=True
    )
    marca = models.CharField(
        max_length=50,editable=True)
    modelo = models.CharField(
        max_length=50, editable=True)
    especificacoes = models.CharField(
        max_length=100, null=True, blank=True, editable=True)
    acesso_remoto = models.CharField(
        max_length=50, null=True, blank=True, editable=True)
    acesso_id = models.CharField(
        max_length=50, null=True, blank=True, editable=True)
    acesso_senha = models.CharField(
        max_length=50, null=True, blank=True, editable=True)
    observacao = models.TextField(
        null=False, blank=True, editable=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    usuario_cadastro = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='equipamentos_criados', null=True)
    data_ultima_alteracao = models.DateTimeField(null=True, default=None)
    usuario_ultima_alteracao = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='equipamento_alterados', null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.tag_patrimonio
    
    class Meta:
        # Ordenando os colaboradores pelo tag_patrimonio por padrão
        ordering = ['tag_patrimonio']


class TransferenciaEmpresa(models.Model):
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    empresa_origem = models.ForeignKey(Empresa, related_name='transferencias_origem', on_delete=models.CASCADE)
    empresa_destino = models.ForeignKey(Empresa, related_name='transferencias_destino', on_delete=models.CASCADE)
    usuario_transferencia_empresa = models.ForeignKey(User, related_name='usuario_transferencia_empresa', on_delete=models.CASCADE)
    data_transferencia = models.DateTimeField(auto_now_add=True)


class TransferenciaColaborador(models.Model):
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    colaborador_origem = models.ForeignKey(Colaborador, related_name='colaborador_origem', on_delete=models.CASCADE)
    colaborador_destino = models.ForeignKey(Colaborador, related_name='colaborador_destino', on_delete=models.CASCADE)
    usuario_transferencia_colaborador = models.ForeignKey(User, related_name='usuario_tranferencia_colaborador', on_delete=models.CASCADE)
    data_transferencia = models.DateTimeField(auto_now_add=True)


class AlteracaiSituacaoEquipamento(models.Model):
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    situacao_anterior = models.CharField(max_length=1, choices=SITUACAO_EQUIPAMENTO_CHOICES)
    situacao_nova = models.CharField(max_length=1, choices=SITUACAO_EQUIPAMENTO_CHOICES)
    usuario_situacao_equipamento = models.ForeignKey(User, related_name='usuario_situacao_equipamento', on_delete=models.CASCADE)
    data_alteracao = models.DateTimeField(auto_now_add=True)


# Método para criar as permissões após as migrações
def create_permissions(sender, **kwargs):
    if sender.name == 'equipamento':
        content_type = ContentType.objects.get_for_model(Equipamento)

        visualizar_equipamento, created = Permission.objects.get_or_create(
            codename = 'visualizar_equipamento',
            name = 'Visualizar Equipamentos',
            content_type = content_type,
        )

        visualiza_detalhe_equipamento, created = Permission.objects.get_or_create(
            codename = 'visualiza_detalhe_equipamento',
            name = 'Visualiar Detalhes do Equipamento',
            content_type = content_type,
        )

        editar_equipamento, created = Permission.objects.get_or_create(
            codename = 'editar_equipamento',
            name = 'Editar Equipamento',
            content_type = content_type,
        )

# Concectar o método ao sinal post_mnigrate
post_migrate.connect(create_permissions)
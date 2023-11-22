from django.db import models

from empresa.models import Empresa
from colaborador.models import Colaborador
from tipo_equipamento.models import TipoEquipamento

# Create your models here.
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
        max_length=20, null=True, blank=True)
    data_compra = models.DateField(
        blank=True, null=True)
    situacao = models.CharField(
        max_length=1, choices=SITUACAO_EQUIPAMENTO_CHOICES, null=False, blank=False)
    empresa = models.ForeignKey(
        Empresa, on_delete=models.PROTECT, limit_choices_to={'status': True})
    colaborador = models.ForeignKey(
        Colaborador, on_delete=models.PROTECT, limit_choices_to={'status': True})
    marca = models.CharField(
        max_length=50)
    modelo = models.CharField(
        max_length=50)
    especificacoes = models.CharField(
        max_length=100, null=True, blank=True)
    acesso_remoto = models.CharField(
        max_length=50, null=True, blank=True)
    acesso_id = models.CharField(
        max_length=50, null=True, blank=True)
    acesso_senha = models.CharField(
        max_length=50, null=True, blank=True)
    observacao = models.TextField(
        null=False, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.tag_patrimonio
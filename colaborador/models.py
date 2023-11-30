from django.db import models
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

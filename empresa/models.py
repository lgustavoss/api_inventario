from django.db import models
from .validators import validar_cnpj


class Empresa(models.Model):
    """
    Modelo para representar as empresas
    """
    # Nome da empresa
    nome = models.CharField(max_length=100, null=False, blank=False)

    # CNPJ da empresa, unico e validado pelo validador validar_cnpj
    cnpj = models.CharField(max_length=18, null=False,blank=False, unique=True, validators=[validar_cnpj])
    
    # Status da empresa, indicando se está ativo ou não (padrão: ativo)
    status = models.BooleanField(default=True)

    class Meta:
        # Ordenando as empresas pelo nome por padrão
        ordering = ['nome']
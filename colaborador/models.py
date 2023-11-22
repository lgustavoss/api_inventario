from django.db import models
from .validators import validar_cpf


class Colaborador(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    cpf = models.CharField(max_length=14, null=False, blank=False, unique=True, validators=[validar_cpf])
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['nome']

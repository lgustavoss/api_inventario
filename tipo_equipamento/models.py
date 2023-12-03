from django.db import models

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
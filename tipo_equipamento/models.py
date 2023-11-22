from django.db import models

# Create your models here.


class TipoEquipamento(models.Model):
    tipo = models.CharField(max_length=100, null=False, blank=False)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['tipo']
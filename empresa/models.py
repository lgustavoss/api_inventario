from django.db import models
from .validators import validar_cnpj

# Create your models here.
class Empresa(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    cnpj = models.CharField(max_length=18, null=False,blank=False, unique=True, validators=[validar_cnpj])
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ['nome']
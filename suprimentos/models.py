from django.db import models
from django.contrib.auth.models import User
from tipo_equipamento.models import TipoEquipamento


class Categoria(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(blank=True, null=True)
    pai = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    # Tipo de equipamento só para categorias pai
    tipo_equipamentos = models.ManyToManyField(TipoEquipamento, blank=True, limit_choices_to={'pai': None})

    data_cadastro = models.DateTimeField(auto_now_add=True)
    usuario_cadastro = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categorias_criadas')
    data_ultima_alteracao = models.DateTimeField(null=True, default=None)
    usuario_ultima_alteracao = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categorias_editadas', null=True)

    def __str__(self):
        return self.nome

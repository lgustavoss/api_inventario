from django.db import models
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from tipo_equipamento.models import TipoEquipamento



class Categoria(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(blank=True, null=True)
    tipo_equipamento = models.ManyToManyField(TipoEquipamento, related_name='categorias')
    status = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    usuario_cadastro = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categorias_criadas')
    data_ultima_alteracao = models.DateTimeField(null=True, default=None)
    usuario_ultima_alteracao = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categorias_editadas', null=True)


class Item(models.Model):
    nome = models.CharField(max_length=255, blank=False, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='item_categoria')
    quantidade = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    usuario_cadastro = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item_criado')
    data_ultima_alteracao = models.DateTimeField(null=True, default=None)
    usuario_ultima_alteracao = models.ForeignKey(User, on_delete=models.CASCADE, related_name='item_editado', null=True)



# Metodo para criar as permissões apos as migracoes
def create_permissions_categoria(sender, **kwargs):
    if sender.name == 'suprimentos':
        content_type = ContentType.objects.get_for_model(Categoria)

        visualizar_categoria, created = Permission.objects.get_or_create(
            codename = 'visualizar_categoria',
            name = 'Visualizar Categorias',
            content_type = content_type,
        )

        visuaiza_detalhe_categoria, created = Permission.objects.get_or_create(
            codename = 'visualiza_detalhe_categoria',
            name = 'Visualizar Detalhes Categoria',
            content_type = content_type,
        )

        editar_categoria, created = Permission.objects.get_or_create(
            codename='editar_categoria',
            name='Editar Categoria',
            content_type=content_type,
        )

def create_permissions_item(sender, **kwargs):
    if sender.name == 'suprimentos':
        content_type = ContentType.objects.get_for_model(Item)

        visualizar_item, created = Permission.objects.get_or_create(
            codename = 'visualizar_item',
            name = 'Visualizar itens',
            content_type = content_type,
        )

        visuaiza_detalhe_item, created = Permission.objects.get_or_create(
            codename = 'visualiza_detalhe_item',
            name = 'Visualizar Detalhes item',
            content_type = content_type,
        )

        editar_item, created = Permission.objects.get_or_create(
            codename='editar_item',
            name='Editar item',
            content_type=content_type,
        )

# Conectar  o metodo ao sinal post_migrate
post_migrate.connect(create_permissions_categoria)
post_migrate.connect(create_permissions_item)
# Generated by Django 4.2.7 on 2024-02-18 22:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tipo_equipamento', '0002_alter_tipoequipamento_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, unique=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('data_ultima_alteracao', models.DateTimeField(default=None, null=True)),
                ('pai', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='suprimentos.categoria')),
                ('tipo_equipamentos', models.ManyToManyField(blank=True, limit_choices_to={'pai': None}, to='tipo_equipamento.tipoequipamento')),
                ('usuario_cadastro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorias_criadas', to=settings.AUTH_USER_MODEL)),
                ('usuario_ultima_alteracao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categorias_editadas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

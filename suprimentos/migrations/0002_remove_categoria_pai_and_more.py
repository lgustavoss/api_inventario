# Generated by Django 4.2.7 on 2024-03-18 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipo_equipamento', '0002_alter_tipoequipamento_options'),
        ('suprimentos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoria',
            name='pai',
        ),
        migrations.RemoveField(
            model_name='categoria',
            name='tipo_equipamentos',
        ),
        migrations.AddField(
            model_name='categoria',
            name='tipo_equipamento',
            field=models.ManyToManyField(related_name='categorias', to='tipo_equipamento.tipoequipamento'),
        ),
    ]

# Generated by Django 4.2.7 on 2024-02-20 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tipo_equipamento', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tipoequipamento',
            options={'ordering': ['id']},
        ),
    ]

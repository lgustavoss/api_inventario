# Generated by Django 4.2.7 on 2024-02-07 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('colaborador', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='colaborador',
            old_name='data_ultima_ateracao',
            new_name='data_ultima_alteracao',
        ),
    ]

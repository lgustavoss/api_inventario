<<<<<<< HEAD
# Generated by Django 4.2.7 on 2024-02-18 22:11
=======
# Generated by Django 4.2.7 on 2024-02-20 19:52
>>>>>>> 14-issue-dashboad-empresa

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('colaborador', '0002_rename_data_ultima_ateracao_colaborador_data_ultima_alteracao'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='colaborador',
            options={'ordering': ['id']},
        ),
    ]

# Generated by Django 4.2.7 on 2024-02-18 22:11
# Generated by Django 4.2.7 on 2024-02-20 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipamento', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipamento',
            options={'ordering': ['tag_patrimonio']},
        ),
    ]

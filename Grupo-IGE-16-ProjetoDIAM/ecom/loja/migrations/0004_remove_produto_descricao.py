# Generated by Django 5.0.6 on 2024-05-09 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0003_alter_produto_nome'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='descricao',
        ),
    ]

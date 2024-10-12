# Generated by Django 5.1.1 on 2024-09-08 17:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
                ('active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('description', models.CharField(max_length=255, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='amount',
            new_name='value',
        ),
        migrations.AddField(
            model_name='account',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Ativo'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Ativo'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='core.category', verbose_name='Categoria'),
            preserve_default=False,
        ),
    ]
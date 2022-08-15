# Generated by Django 4.1 on 2022-08-15 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('codigo_de_barras', models.BigIntegerField(blank=True, null=True)),
                ('preco_de_venda', models.DecimalField(decimal_places=2, max_digits=10)),
                ('preco_de_custo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('unidade_de_venda', models.CharField(choices=[('UND', 'Unidade'), ('CX', 'Caixa'), ('KG', 'Quilograma'), ('LT', 'Litro'), ('MT', 'Metro Linear'), ('M2', 'Metro Quadrado'), ('M3', 'Metro Cubico')], max_length=3)),
                ('data_de_cadastro', models.DateTimeField(auto_now_add=True)),
                ('ultima_atualizacao', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=0)),
                ('ultima_entrada', models.DateTimeField(blank=True, default=None, null=True)),
                ('ultima_saida', models.DateTimeField(blank=True, default=None, null=True)),
                ('produto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='estoque', to='api.produto')),
            ],
        ),
    ]

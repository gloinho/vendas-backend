from decimal import Decimal
from tabnanny import verbose
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.

class Produto(models.Model):
    UNIDADE_DE_VENDA_CHOICES = (
        ('UND','Unidade'),
        ('CX', 'Caixa'),
        ('KG', 'Quilograma'),
        ('LT', 'Litro'),
        ('MT', 'Metro Linear'),
        ('M2', 'Metro Quadrado'),
        ('M3', 'Metro Cubico'),
    )
     
    nome = models.CharField(verbose_name='Nome',max_length=100, null=False, blank=False)
    codigo_de_barras = models.BigIntegerField(verbose_name='Código de Barras',null=True, blank=True, unique=True)
    preco_de_venda = models.DecimalField(verbose_name="Preço de Venda", decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0.01'))])
    preco_de_custo = models.DecimalField(verbose_name="Preço de Custo", decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0.01'))])
    unidade_de_venda = models.CharField(
        verbose_name="Unidade de Venda",
        max_length=3,
        choices=UNIDADE_DE_VENDA_CHOICES)
    data_de_cadastro = models.DateTimeField(verbose_name="Data de Cadastro", auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(verbose_name="Última Atualização", auto_now=True)
    
    def __str__(self):
        return self.nome

class Estoque(models.Model):
    
    produto = models.OneToOneField(
        Produto, on_delete=models.CASCADE, related_name='estoque')
    quantidade = models.PositiveIntegerField(default=0)
    ultima_entrada = models.DateTimeField(default=None, null=True, blank=True)
    ultima_saida = models.DateTimeField(default=None, null=True, blank=True)
    
    def __str__(self):
        return f'{self.produto.nome}'
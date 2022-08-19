from decimal import Decimal
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed


# Create your models here.

class Produto(models.Model):
    UNIDADE_DE_VENDA_CHOICES = (
        ('UND','Unidade'),
        ('CX', 'Caixa'),
        ('KG', 'Quilograma'),
        ('LT', 'Litro'),
        ('MT', 'Metro Linear'),
        ('MT2', 'Metro Quadrado'),
        ('MT3', 'Metro Cubico'),
    )
     
    nome = models.CharField(
        verbose_name='Nome',max_length=100, null=False, blank=False)
    codigo_de_barras = models.BigIntegerField(
        verbose_name='Código de Barras',null=True, blank=True, 
        unique=True,
        error_messages={'unique':'Este código de barras já está cadastrado'})
    preco_de_venda = models.DecimalField(
        verbose_name="Preço de Venda", decimal_places=2, max_digits=10, 
        validators=[MinValueValidator(Decimal('0.01'))])
    preco_de_custo = models.DecimalField(
        verbose_name="Preço de Custo", decimal_places=2, max_digits=10, 
        validators=[MinValueValidator(Decimal('0.01'))])
    unidade_de_venda = models.CharField(
        verbose_name="Unidade de Venda",
        max_length=3,
        choices=UNIDADE_DE_VENDA_CHOICES)
    data_de_cadastro = models.DateTimeField(
        verbose_name="Data de Cadastro", auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(
        verbose_name="Última Atualização", auto_now=True)
   
    def __str__(self):
        return self.nome

class Estoque(models.Model):
    
    produto = models.OneToOneField(
        Produto, on_delete=models.CASCADE, related_name='estoque')
    quantidade = models.PositiveIntegerField(
        default=0, 
        validators=[MinValueValidator(0)], 
        error_messages={'Erro':'A quantidade deve ser positiva'})
    ultima_entrada = models.DateTimeField(default=None, null=True, blank=True)
    ultima_saida = models.DateTimeField(default=None, null=True, blank=True)
    
    def __str__(self):
        return f'{self.produto.nome}'
    
class Historico(models.Model):
    TIPO_CHOICES = (
        ('Entrada','Entrada'),
        ('Saida','Saída'),
        ('Reajuste','Reajuste'),
    )
    produto = models.ForeignKey(
        Produto, verbose_name="Histórico", on_delete=models.CASCADE, related_name='historico')
    quantidade = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    data = models.DateTimeField(default=timezone.now)
    tipo = models.CharField(max_length=8,choices=TIPO_CHOICES)
    
    def __str__(self):
        return f'{self.produto} tipo {self.tipo}'
     
   
class Venda(models.Model):
    SITUACAO_CHOICES = (
        ('Fechada','Fechada'),
        ('Cancelada','Cancelada')
    )
    PAGAMENTO_CHOICES = (
        ('Pix','Pix'),
        ('Dinheiro','Dinheiro'),
        ('Cartão','Cartão'), 
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data = models.DateTimeField(default=timezone.now)
    itens = models.ManyToManyField(Produto, related_name='venda')
    situacao = models.CharField(choices=SITUACAO_CHOICES, default='Fechada', max_length=9)
    
    def __str__(self):  
        return f'Venda {self.id}'

    
class ItensVenda(models.Model):
    # Previne que o item seja deletado se estiver em uma venda.
    
    item = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='itens_venda')
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='venda_itens')
    
    def __str__(self):
        return f'Item da venda {self.venda}'

# Signal para popular o total de uma venda e adicionar os itens selecionados
# no Model ItensVenda
def VendaReceiver(instance, sender, action,**kwargs):
    total = 0
    if action in ['post_add']:
        for item in instance.itens.all():
            total += item.preco_de_venda
            ItensVenda.objects.create(item=item, venda=instance)
    instance.total = total
    instance.save()
       
m2m_changed.connect(VendaReceiver, sender=Venda.itens.through)
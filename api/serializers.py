from rest_framework import serializers
from api.models import Estoque, Produto, Historico
from django.utils import timezone


class CreateProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = [
            'nome',
            'codigo_de_barras',
            'preco_de_venda',
            'preco_de_custo',
            'unidade_de_venda',
        ]
     
class RetrieveUpdateProdutoSerializer(serializers.ModelSerializer):
    data_de_cadastro = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    ultima_atualizacao = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    ultima_entrada = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, source="estoque.ultima_entrada")
    ultima_saida = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, source="estoque.ultima_saida")
    class Meta:
        model = Produto
        fields =[
            'id','nome','codigo_de_barras','preco_de_venda','preco_de_custo',
            'unidade_de_venda','data_de_cadastro','ultima_atualizacao',            
            'ultima_entrada','ultima_saida','estoque'
        ]
        
class RetrieveEstoqueSerializer(serializers.ModelSerializer):
    nome_do_produto = serializers.CharField(source="produto.nome")
    ultima_entrada = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    ultima_saida = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    class Meta:
        model = Estoque
        fields =[
            'id','nome_do_produto','produto', 'quantidade','ultima_entrada','ultima_saida'
        ]

class HistoricoSerializer(serializers.ModelSerializer):
    nome_do_produto = serializers.CharField(source="produto.nome", read_only=True)
    data = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    class Meta:
        model = Historico
        fields = [
            'id',
            'nome_do_produto',
            'produto',
            'tipo',
            'data',
            'quantidade'
        ]
       
class UpdateEstoqueSerializer(serializers.ModelSerializer):
    
    funcao = serializers.ChoiceField(choices=['drenagem','adicao','atualizacao'], write_only=True)
    
    class Meta:
        model = Estoque
        fields = [
            'quantidade',
            'funcao'
        ]
    def update(self, instance, validated_data):
        # Todo movimento de estoque deve gerar um histórico correspondente.
        
        # Movimento tipo drenagem -> Tipo de histórico = Saída -- Atualizar ultima saída na instance
            # # Subtrai do valor atual do estoque
        # Movimento tipo adição -> Tipo de histórico = Entrada -- Atualizar ultima entrada na instance
            # # Adiciona ao valor atual do estoque
        # Movimento tipo atualização -> Tipo de histórico = Reajuste -- Atualizar ultima entrada ou saída na instance
            # # Substitui o valor atual do estoque.
        
        tipo_movimento = validated_data.get('funcao')
        quantidade_movimento = validated_data.get('quantidade')
        produto = instance.produto
        quantidade_atual = instance.quantidade
        
        
        if tipo_movimento == 'atualizacao':
            Historico.objects.create(produto=produto, quantidade = quantidade_movimento, tipo='Reajuste')
            if quantidade_atual > quantidade_movimento: # SAÍDA / REAJUSTE
                instance.ultima_saida = timezone.now()
            else:
                instance.ultima_entrada = timezone.now()
                
        if tipo_movimento == 'drenagem':
            validated_data['quantidade'] = quantidade_atual - quantidade_movimento
            if validated_data.get('quantidade') < 0:
                raise serializers.ValidationError([{'Erro':'Estoque não pode ser negativo'}])
            Historico.objects.create(produto=produto, quantidade = quantidade_movimento, tipo='Saida')
            instance.ultima_saida = timezone.now()
            
        if tipo_movimento == 'adicao':
            Historico.objects.create(produto=produto, quantidade = quantidade_movimento, tipo='Entrada')
            instance.ultima_entrada = timezone.now()
            validated_data['quantidade'] = quantidade_atual + quantidade_movimento
        
        validated_data.pop('funcao', None)
        return super().update(instance, validated_data)
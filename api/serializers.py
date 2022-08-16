from rest_framework import serializers
from api.models import Estoque, Produto


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
    class Meta:
        model = Produto
        fields =[
            'id','nome','codigo_de_barras','preco_de_venda','preco_de_custo',
            'unidade_de_venda','data_de_cadastro','ultima_atualizacao'
        ]
        
class RetrieveEstoqueSerializer(serializers.ModelSerializer):
    ultima_entrada = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    ultima_saida = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    class Meta:
        model = Estoque
        fields =[
            'produto', 'quantidade','ultima_entrada','ultima_saida'
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
        
        validated_data.pop('funcao', None)
        return super().update(instance, validated_data)
from rest_framework import serializers
from api.models import Produto


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = [
            'nome',
            'codigo_de_barras',
            'preco_de_venda',
            'preco_de_custo',
            'unidade_de_venda',
        ]
        
class VerProdutoSerializer(serializers.ModelSerializer):
    data_de_cadastro = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    ultima_atualizacao = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    class Meta:
        model = Produto
        fields =[
            'id','nome','codigo_de_barras','preco_de_venda','preco_de_custo',
            'unidade_de_venda','data_de_cadastro','ultima_atualizacao'
        ]
        

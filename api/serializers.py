from rest_framework.serializers import ModelSerializer
from api.models import Produto

class ProdutoSerializer(ModelSerializer):
    class Meta:
        model = Produto
        fields = [
            'nome',
            'codigo_de_barras',
            'preco_de_venda',
            'preco_de_custo',
            'unidade_de_venda',
        ]
        
class VerProdutoSerializer(ModelSerializer):
    class Meta:
        model = Produto
        fields =[
            'pk','nome','codigo_de_barras','preco_de_venda','preco_de_custo',
            'unidade_de_venda','data_de_cadastro','ultima_atualizacao'
        ]
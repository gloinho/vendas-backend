from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Produto, Estoque
from api.serializers import ProdutoSerializer, VerProdutoSerializer

# Create your views here.

@api_view(['POST'])
def CadastroDeProduto(request):
    serializer = ProdutoSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        produto = Produto.objects.get(nome=serializer.validated_data.get('nome'))
        estoque_inicial = serializer.validated_data.get('estoque_inicial')
        if estoque_inicial:
            Estoque.objects.create(produto=produto, quantidade = estoque_inicial)
        Estoque.objects.create(produto=produto, quantidade = 0)
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['GET'])
def VerProduto(request, pk):
    instance = Produto.objects.get(pk=pk)
    serializer = VerProdutoSerializer(instance=instance)
    return Response(serializer.data)
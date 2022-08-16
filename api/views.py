from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django_filters import rest_framework as filters
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
        return Response({"success":"Produto cadastrado com sucesso"})
    return Response(serializer.errors)

@api_view(['PUT','GET'])
def VerProduto(request, pk):
    if request.method == 'GET':
        instance = Produto.objects.get(pk=pk)
        serializer = VerProdutoSerializer(instance=instance)
        return Response(serializer.data)
    if request.method == 'PUT':
        instance = Produto.objects.get(pk=pk)
        serializer = VerProdutoSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(status=status.HTTP_200_OK)
            
class ProdutoFilter(filters.FilterSet):
    class Meta:
        model = Produto
        fields = {
            'codigo_de_barras': ['contains'],
            'nome': ['contains']
        }
        
class ListTodosOsProdutosAPIView(generics.ListAPIView):
    queryset = Produto.objects.all()
    serializer_class = VerProdutoSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProdutoFilter



    


    
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from django_filters import rest_framework as filters
from django.utils import timezone

from api.models import Produto, Estoque
from api.serializers import CreateProdutoSerializer, RetrieveUpdateProdutoSerializer, RetrieveEstoqueSerializer, UpdateEstoqueSerializer


# Create your views here.

@api_view(['POST'])
def CreateProduto(request):
    serializer = CreateProdutoSerializer(data=request.data)
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
def RetrieveUpdateProduto(request, pk):
    if request.method == 'GET':
        instance = Produto.objects.get(pk=pk)
        serializer = RetrieveUpdateProdutoSerializer(instance=instance)
        return Response(serializer.data)
    if request.method == 'PUT':
        instance = Produto.objects.get(pk=pk)
        serializer = RetrieveUpdateProdutoSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"Produto atualizado com sucesso"})   
        return Response(serializer.errors)
            
class ProdutoFilter(filters.FilterSet):
    class Meta:
        model = Produto
        fields = {
            'codigo_de_barras': ['contains'],
            'nome': ['contains']
        }
        
class ListTodosOsProdutos(generics.ListAPIView):
    queryset = Produto.objects.all()
    serializer_class = RetrieveUpdateProdutoSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProdutoFilter

@api_view(['GET','PUT'])
def RetrieveUpdateEstoque(request, pk):
    if request.method == 'GET':
        instance = Estoque.objects.get(pk=pk)
        serializer = RetrieveEstoqueSerializer(instance=instance)
        return Response(serializer.data)
    if request.method == 'PUT':
        instance = Estoque.objects.get(pk=pk)
        serializer = UpdateEstoqueSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            print(request.data)
            data = serializer.validated_data
            if instance.quantidade > data['quantidade'] and data['funcao'] == 'drenagem' or data['funcao'] == 'atualizacao':
                data['ultima_saida'] = timezone.now()
                print(data)
            elif instance.quantidade < data['quantidade'] and data['funcao'] == 'adicao' or data['funcao'] == 'atualizacao':
                data['ultima_entrada'] = timezone.now()
                print(data)
            serializer.save()
        return Response(serializer.data)
    

    


    
    
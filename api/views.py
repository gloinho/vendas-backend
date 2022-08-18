from dataclasses import field
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
        estoque_inicial = request.data.get('estoque_inicial')
        serializer.save()
        produto = Produto.objects.last()
        if estoque_inicial != 0:
            Estoque.objects.create(produto=produto, quantidade = estoque_inicial)
        else:
            Estoque.objects.create(produto=produto)
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
            'nome': ['contains'],
            'estoque__ultima_entrada':['lt','gt'],
            'estoque__ultima_saida':['lt','gt']
        }

class ListTodosOsProdutos(generics.ListAPIView):
    queryset = Produto.objects.all()
    serializer_class = RetrieveUpdateProdutoSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProdutoFilter

class EstoqueFilter(filters.FilterSet):
    class Meta:
        model = Estoque 
        fields= {
            'produto__codigo_de_barras':['contains'],
            'produto__nome':['contains'],
            'quantidade':['exact'],   
        }

class ListTodosOsEstoques(generics.ListAPIView):
    queryset = Estoque.objects.all()
    serializer_class = RetrieveEstoqueSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EstoqueFilter
    
@api_view(['GET','PUT'])
def RetrieveUpdateEstoque(request, pk):
    if request.method == 'GET':
        instance = Estoque.objects.get(pk=pk)
        serializer = RetrieveEstoqueSerializer(instance=instance)
        return Response(serializer.data)
    if request.method == 'PUT':
        instance = Estoque.objects.get(pk=pk)
        serializer = UpdateEstoqueSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.update(instance=instance, validated_data=serializer.validated_data)
            return Response([{"Sucesso":"Estoque atualizado com sucesso."}])
        return Response(serializer.errors)
    

    


    
    
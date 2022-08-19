from django.urls import path
from api.views import CreateProduto, RetrieveUpdateProduto, ListTodosOsProdutos, RetrieveUpdateEstoque, ListTodosOsEstoques, ListHistorico

app_name = 'api'

urlpatterns = [
    path('cadastro',CreateProduto, name="cadastro-de-produto"),
    path('produto/<int:pk>', RetrieveUpdateProduto, name="ver-produto"),
    path('produto/<int:pk>/estoque', RetrieveUpdateEstoque, name="ver-estoque"),
    path('historicos', ListHistorico.as_view(), name="ver-todos-os-historicos"),
    path('produtos', ListTodosOsProdutos.as_view(), name='ver-todos-os-produtos'),
    path('estoques', ListTodosOsEstoques.as_view(), name='ver-todos-os-estoques')
]
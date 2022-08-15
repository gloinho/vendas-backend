from django.urls import path
from api.views import CadastroDeProduto, VerProduto, VerTodosOsProdutos

app_name = 'api'

urlpatterns = [
    path('cadastro',CadastroDeProduto, name="cadastro-de-produto"),
    path('produto/<int:pk>', VerProduto, name="ver-produto"),
    path('produtos', VerTodosOsProdutos, name='ver-todos-os-produtos'),
]
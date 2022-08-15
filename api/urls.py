from argparse import Namespace
from django.urls import path
from api.views import CadastroDeProduto, VerProduto

app_name = 'api'

urlpatterns = [
    path('cadastro',CadastroDeProduto, name="cadastro-de-produto"),
    path('produto/<int:pk>', VerProduto, name="ver-produto")
]
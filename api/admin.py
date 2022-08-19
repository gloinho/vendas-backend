from django.contrib import admin
from api.models import Historico, ItensVenda, Produto, Estoque, Venda
# Register your models here.

admin.site.register(Produto)
admin.site.register(Estoque)
admin.site.register(Historico)
admin.site.register(Venda)
admin.site.register(ItensVenda)
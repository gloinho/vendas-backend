from django.contrib import admin
from api.models import Historico, Produto, Estoque
# Register your models here.

admin.site.register(Produto)
admin.site.register(Estoque)
admin.site.register(Historico)
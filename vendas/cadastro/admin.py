from django.contrib import admin
from .models import *

@admin.register(Cadastro)
class  CadastrosrAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'cpf', 'email', 'phone', 'birthday', 'created')
    date_hierarchy = 'created'
    search_fields = ('firstname', 'lastname')

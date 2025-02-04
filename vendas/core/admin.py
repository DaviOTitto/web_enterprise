from django.contrib import admin,messages
from .models import *
from import_export.admin import ExportActionMixin,ImportExportModelAdmin
from django.urls import path
from django.shortcuts import redirect

    
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    ordering = ['produto_pro']
    list_display = ('produto_pro','descricao_pro','unidade_pro','grupo_pro',
                    'sigla_fab_pro','trib_pro','taxa_pro','obs_pro')
    list_filter = ('grupo_pro',)
    search_fields = ('descricao_pro',)

@admin.register(NCM_CEST)
class NCM_CESTAdmin(admin.ModelAdmin):
    ordering = ['NCM_cabec']
    list_display =('NCM_cabec','codigo_ncm_sh','codigo_Cest','descricao_cest',
                    'Ncm_calc_pob','MVa_original')
    search_fields =('codigo_ncm_sh',)


class ItemVENInline(admin.TabularInline):
    list_display = ['product', 'quantity', 'price_sale']
    readonly_fields = ['get_subtotal']
    model = ItemVEN
    extra = 0

@admin.register(Titulos)
class Titulosadmim(admin.ModelAdmin):
    ordering = ['data_emissao_tit']
    list_display = ['numero_tit','data_emissao_tit','tipo_tit']
    models = Titulos 
    search_fields = ('data_emissao_tit',)

@admin.register(SetorPRO)
class SetorPROadimn(admin.ModelAdmin):
    ordering=['num_setor']
    list_display=('cod_pro_set','num_setor','preco_venda_set')
    model=SetorPRO
    search_fields=('num_setor',)

@admin.register(Mov_caixa)
class finamAdmin(admin.ModelAdmin):
    ordering= ['id_mov_Caixa']
    list_display= ('id_mov_Caixa','data_mov','Troco_inicial')
    model = Mov_caixa
    search_fields = ('data_mov',)
    #actions= [duplicate_MVN]


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'cliente_ven_id', 'data_ven', 'get_itens', 'get_total')
    readonly_fields = ['get_total']
    date_hierarchy = 'datainc_ven'
    list_filter = ('cliente_ven_id',)
    inlines = [ItemVENInline]


@admin.register(CondPag)
class CondpagADmin(admin.ModelAdmin):
    ordering = ['codigo',]
    list_display = (
        '__str__', 'codigo', 'descricao', 'juros', 'tipo_juros','nao_aceitar_desc')
    search_fields = ('codigo',)

@admin.register(Estado)
class EstadoAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('sigla_est','nome_est','icms_com_est','icms_ven_est',
                    'usuario_est','dif_aliquota_est',
                    'mva_estado')
    search_fields = ('sigla_est',)

@admin.action(description='Duplicar grupo selecionado')
def duplicate(ModelAdmin, request, queryset):
    for object in queryset:
        object.codigo_gru = None
        object.save()
    duplicate.short_description = "Duplicar grupo selecionado"
    messages.add_message(
        request,
        messages.INFO,
        'Registro Duplicado.'
        )
    return redirect('admin:core_grupopro_changelist')
def duplicate_MVN(ModelAdmin, request, queryset):
    for object in queryset:
        object.id_mov_caixa = None
        object.save()
    duplicate.short_description = "Duplicar movimento selecionado"
    messages.add_message(
        request,
        messages.INFO,
       'Registro Duplicado.'
        )
    return redirect('admin:core_ID_MOV_CAIXA_changelist')


@admin.register(GrupoPRO)
class GrupoPROAdmin(ExportActionMixin,admin.ModelAdmin):
    ordering = ['codigo_gru']
    list_display = ('desc_gru','cod_interligacao_gru','tipo_desconto_gru','lojavirt_gru',
                    'garantia_mercadolivre_gru','categoria_mercadolivre_gru')
    search_fields = ('desc_gru',)    
#MODIFICADO ANTONIO 23/05/22
    list_editable  = ( 'lojavirt_gru',)
    actions = [duplicate]
#Modificado Davi Oliveira 26/05/2022
@admin.register(Unidade)
class UnidadeAdmin(ExportActionMixin,admin.ModelAdmin):
    ordering = ['id_uni']
    list_display = ('__str__','id_uni','unidade_uni','descricao_uni','sigla_uni','un_tiss_uni')
    search_fields = ('id_uni',)    
    list_editable  = ( 'descricao_uni',)
    actions = [duplicate]


@admin.action(description='Duplicar tipo selecionado')
def duplicate_tipo(ModelAdmin, request, queryset):
    for object in queryset:
        object.cod_tip_pro = None
        object.save()
    duplicate.short_description = "Duplicar tipo selecionado"
    messages.add_message(
        request,
        messages.INFO,
        'Registro Duplicado.'
        )
    return redirect('admin:core_tipopro_changelist')


@admin.register(TipoPRO)
#modfificado para os parametros da table original , Davi Oliveira Tito 10/05/2022
class TipoPROAdmin(ExportActionMixin,admin.ModelAdmin):
    ordering = ['cod_tip_pro']
    list_display = ('cod_tip_pro','key_tip','desc_tip','desconto_max_tip',
                    'transmitido','mostrar_msg_tip')
    search_fields = ('key_tp',)  
    list_editable  = ( 'transmitido',)
    actions = [duplicate_tipo] 
#adicionado cupom, Davi Oliveira Tito 10/05/2022
#adcionado customerAdmin DAvi 20/06/2022
@admin.register(Cadastro)
class  CadastrosAdmin(ExportActionMixin,admin.ModelAdmin):
    ordering=['codigo_cad']
    list_display=('codigo_cad','nome_cad','rua1_cad','bairro1_cad','cidade1_cad','contato_cad')
    search_fields = ('nome_cad',)
    #actions = [duplicate_tipo]
@admin.register(Setor)
class SetorADmin(ExportActionMixin,admin.ModelAdmin):
    ordering= ['key_setor']
    list_display = ('key_setor','desc_setor','cadastro_setor','sep_setor','area_servico_setor','agrup_contas_setor')
    search_fields= ('desc_setor',)
    

@admin.register(cupom)
class cupomAdmin(admin.ModelAdmin):
    ordering = ['id_cupom']
    list_display =( 'id_cupom','valor_cupom','nome_cupom','setor_do_pro','data_inic','data_fim')
    search_fileds = ('nome_cupom',)
    actions = [duplicate_tipo]
from django import forms

from .models import *
from vendas.users.models import User
from rest_framework import serializers


class ImagemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seguranc
        fields = '__all__'
class  CadastrosForm(forms.ModelForm):
    class Meta:
        model =  Cadastro
        fields = '__all__'
class TItulosForm(forms.ModelForm):
    class Meta:
        model = Titulos
        fields= '__all__'
   
#modificado Davi Oliveira TIto. 04/07class VendaForm(forms.ModelForm):
#class VendaForm(forms.ModelForm):    
    #class meta:
       # model= Venda
       # files ='__all__'


class VendaForm(forms.ModelForm):
    cliente_ven_aux_cod = forms.CharField(label='Cód.',widget=forms.TextInput(attrs={'size':'2','autocomplete':'off'}),initial=538)
    cliente_ven_aux_nome = forms.CharField(label='Nome do Cliente',widget=forms.TextInput(attrs={'size':'40','autocomplete':'off'}),initial='CLIENTE CONSUMIDOR',disabled=True)
    cliente_ven_aux_cpf = forms.CharField(label='CNPJ ou CPF',widget=forms.TextInput(attrs={'size':'15','autocomplete':'off'}),initial='11111111111',disabled=True)
    cliente_ven_aux_nasc = forms.CharField(label='Nascimento',widget=forms.TextInput(attrs={'size':'10','autocomplete':'off'}),initial='30/12/1899',disabled=True)
    formapag_ven_aux_cod = forms.CharField(label='Cód.',widget=forms.TextInput(attrs={'size':'2','autocomplete':'off'}),initial=60)
    formapag_ven_aux_nome = forms.CharField(label='Forma de pagamento',widget=forms.TextInput(attrs={'size':'40','autocomplete':'off'}),initial="a vista", disabled=True,required=False)
    acrescimo_ven = forms.DecimalField(label='Acréscimo',widget=forms.NumberInput(attrs={'step':'0.01','value':'0','min':'0'}))
    desconto_ven = forms.DecimalField(label='Desconto',widget=forms.NumberInput(attrs={'step':'0.01','value':'0','min':'0'}))
    class Meta:
        model = Venda
        fields = ('numero_ven','cliente_ven_aux_nome','cliente_ven_aux_cpf','cliente_ven_aux_nasc',
                'formapag_ven_aux_nome')
    
    field_order = ('cliente_ven_aux_cod','cliente_ven_aux_nome','cliente_ven_aux_cpf',
                  'cliente_ven_aux_nasc','formapag_ven_aux_cod','formapag_ven_aux_nome',
                  'acrescimo_ven','desconto_ven','valor_pago')


class ItemVenForm(forms.ModelForm):
    produto_ite_aux_cod = forms.CharField(label='Cód.',widget=forms.TextInput(attrs={'size':'2','autocomplete':'off'}))
    produto_ite_aux_nome = forms.CharField(label='Nome do Produto',widget=forms.TextInput(attrs={'size':'40','autocomplete':'off'}),disabled=True,required=False)
    produto_ite_aux_valor = forms.DecimalField(label='valor do unitario do produto',widget=forms.NumberInput(attrs={'step':'0.01','value':'1','min':'1','autocomplete':'off'}))
    produto_ite_aux_quant = forms.DecimalField(label='quantidade desejada',widget=forms.NumberInput(attrs={'step':'0.1','value':'1','min':'1','autocomplete':'off'}))
    #setPRO_ite_aux_n ita = forms.DecimalField(label='valor do Produto',widget=forms.NumberInput(attrs={'step':'0.01','value':'0','min':'1'}),disabled=True,required=False)
    class Meta:
        model = ItemVEN
        fields = ('produto_ite_aux_cod','produto_ite_aux_nome','produto_ite_aux_quant','produto_ite_aux_valor')

        field_order = ('produto_ite_aux_cod','produto_ite_aux_nome','produto_ite_aux_valor','produto_ite_aux_quant')


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
class Mov_caixaForm(forms.ModelForm):
     class Meta:
        model = Mov_caixa
        fields = '__all__'

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'


class SetorProForm(forms.ModelForm):
    class Meta:
        model = SetorPRO
        exclude = ('Codigo_PRO_SETPRO',)
#        exclude = ('Codigo_SET_SETPRO','Codigo_PRO_SETPRO')


class GrupoproForm(forms.ModelForm):
   
    class Meta:
        model = GrupoPRO
        exclude = ('codigo_gru','cod_interligacao_gru','ult_usuario_gru','ult_data_gru', 'ult_hora_gru')
        field_order = ('desc_gru')


class TipoPROForm(forms.ModelForm):

    class Meta:
        model = TipoPRO
        fields = '__all__'

class UnidadeForm(forms.ModelForm):

    class Meta:
        model = Unidade
        fields = '__all__'


class cupomForm(forms.ModelForm):

    class Meta:
        model = cupom
        fields = '__all__'
class NCM_CEST(forms.ModelForm):

    class Meta:
        model = NCM_CEST
        fields = '__all__'

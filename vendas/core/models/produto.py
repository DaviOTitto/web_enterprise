import uuid
import re
from django.db import models
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, resolve_url, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.utils.formats import number_format
from django.utils import timezone
from vendas.users.models import User
import datetime
from ..models import *
#from .models import *
#from django.contrib import admin, messages
#from import_export.admin import ExportActionMixin,ImportExportModelAdmin
#modificado Antonio 23/05/2022


loja_virt_list = [('S','sim'),('N','Não')]

class Estado(models.Model):
    sigla_est = models.CharField('Sigla do Estado (UF)',max_length=2,null=False,primary_key=True,help_text="Unidade Federativa")
    nome_est = models.CharField('Nome do Estado',max_length=35,help_text="Nome da unidade federativa")
    icms_com_est = models.DecimalField('Alíquota ICMS para venda',max_digits=7,decimal_places=2,help_text="Porcentagem para calculo de venda")
    icms_ven_est = models.DecimalField('Alíquota ICMS para compra',max_digits=7,decimal_places=2,help_text="Porcentagem para calculo de compra")
    usuario_est = models.IntegerField('Codigo do Usuario',editable=False)
 #   data_est = models.DateTimeField('Data alteraçao',editable=False,default=timezone.now)
 #   hora_est = models.DateTimeField('Hora alteracao',editable=False,default=timezone.now)
    dif_aliquota_est = models.DecimalField('Diferença de aliquota',max_digits=7,null=True,decimal_places=2, help_text="Afeta no cálculo das comissões e limites de desconto")
    mva_estado = models.DecimalField('MVA Estado',max_digits=7,decimal_places=2,editable=False)

    class Meta:
        ordering = ['sigla_est']
        verbose_name = 'Estado'

    def __str__(self):
        return self.nome_est

class Produto(models.Model):
    produto_pro = models.AutoField('Código do produto',primary_key=True)
    descricao_pro = models.CharField('Descrição',max_length=60,null=True,blank=True)
    unidade_pro = models.CharField('Unidade',max_length=5,null=True,blank=True)
    cod_fab_pro = models.DecimalField('Código do fabricante',max_digits=7,decimal_places=2,null=True,blank=True)
    custo_med_pro = models.DecimalField('Custo médio',max_digits=7,decimal_places=2,null=True,blank=True)
    margem_lucro_pro = models.DecimalField('Margem de lucro',max_digits=7,decimal_places=2,null=True,blank=True)
    qtd_minima_pro = models.DecimalField('Quantidade minima',max_digits=7,decimal_places=2,null=True,blank=True)
    min_automat_pro = models.CharField('Quantidade minima automático',max_length=1,null=True,blank=True)
    lote_min_pro = models.DecimalField('Lote minimo',max_digits=7,decimal_places=2,null=True,blank=True)
    curva_pro = models.CharField('Curva do produto', max_length=1,null=True,blank=True)
    peso_liq_pro = models.DecimalField('Peso líquido',max_digits=7,decimal_places=2,null=True,blank=True)
    med_entrega_pro = models.DecimalField('Medidas entrega',max_digits=7,decimal_places=2,null=True,blank=True)
    tipo_pro = models.CharField('Tipo do produto',max_length=3,null=True,blank=True)
    trib_pro = models.DecimalField('Tributo',max_digits=7,decimal_places=2,null=True,blank=True)
    taxa_pro = models.DecimalField('Taxa',max_digits=7,decimal_places=2,null=True,blank=True)
    sigla_fab_pro = models.CharField('Sigla de Fábrica',max_length=15,null=True,blank=True)
    grupo_pro = models.DecimalField('Grupo',max_digits=7,decimal_places=2,null=True,blank=True)
    foto_pro =  models.ImageField('Foto',upload_to='produtos/',null=True,blank=True)
    trib_ipi_pro = models.IntegerField('Tributo IPI',null=True,blank=True)
    taxa_ipi_pro = models.IntegerField('Taxa IPI',null=True,blank=True)
    indice_1_pro = models.DecimalField('Indice 1',max_digits=7,decimal_places=2,null=True,blank=True)
    indice_2_pro = models.DecimalField('Indice 2',max_digits=7,decimal_places=2,null=True,blank=True)
    ult_usuario_pro = models.IntegerField('Último usuário',null=True,blank=True)
    ult_data_pro = models.DateTimeField('Data ultima alteracao',null=True,blank=True,default=timezone.now)
    ult_hora_pro = models.DateTimeField('Hora ultima alteracao',null=True,blank=True,default=timezone.now)
    obs_pro = models.TextField('Observações',blank=True,null=True)
    comis_max_pro = models.DecimalField('Comissão máxima',max_digits=7,decimal_places=2,null=True,blank=True)
    comis_min_pro = models.DecimalField('Comissão mínima',max_digits=7,decimal_places=2,null=True,blank=True)
    desc_limite_pro = models.DecimalField('Desconto limite',max_digits=7,decimal_places=2,null=True,blank=True)
    desc_maximo_pro = models.DecimalField('Desconto maximo',max_digits=7,decimal_places=2,null=True,blank=True)
    atacado_pro = models.DecimalField('Atacado',max_digits=7,decimal_places=2,null=True,blank=True)
    imp_etiqueta_pro = models.CharField('Impressao de etiqueta',max_length=1,null=True,blank=True)
    imp_lista_pro = models.CharField('Impressao de lista',max_length=1,null=True,blank=True)
    cod_icms_imp_pro = models.IntegerField('Código do ICMS impressão',null=True,blank=True)
    cod_interligacao_pro = models.CharField('Código de interligação',max_length=15,null=True,blank=True)
    preco_promocao_pro = models.DecimalField('Preço Promoção',max_digits=7,decimal_places=2,null=True,blank=True)
    transmitido_pro = models.CharField('Transmitido',max_length=1,null=True,blank=True)
    cor_pro = models.DecimalField('Cor',max_digits=7,decimal_places=2,null=True,blank=True)
    classificacao_pro = models.CharField('Classificação',max_length=1,null=True,blank=True)
    msg_fora_uf_pro = models.CharField('Mensagem para fora UF',max_length=1,null=True,blank=True)
    padrao_tiss_pro = models.CharField('Padrão TISS',max_length=12,null=True,blank=True)
    cod_tab_tiss_pro = models.CharField('Código padrão tiss',max_length=2,null=True,blank=True)
    impostos_pro = models.DecimalField('Impostos',max_digits=7,decimal_places=2,null=True,blank=True)
    descont_custo_medio_pro = models.CharField('Desconto custo médio',max_length=1,null=True,blank=True)
    nao_bloquear_pro = models.CharField('Não bloquear',max_length=1,null=True,blank=True)
    producao_prop_pro = models.CharField('Produção proposta',max_length=1,null=True,blank=True)
    cnae_pro = models.CharField('CNAE',max_length=10,null=True,blank=True)
    cod_trib_munic_pro = models.CharField('Código tributo municipal',max_length=6,null=True,blank=True)
    mrepos_pro = models.IntegerField('MRepos',null=True,blank=True)
    altura_pro = models.DecimalField('Altura do produto',max_digits=7,decimal_places=2,null=True,blank=True)
    largura_pro = models.DecimalField('Largura do produto',max_digits=7,decimal_places=2,null=True,blank=True)
    comprimento_pro = models.DecimalField('Comprimento do produto',max_digits=7,decimal_places=2,null=True,blank=True)
    diametro_pro = models.DecimalField('Diametro do produto',max_digits=7,decimal_places=2,null=True,blank=True)
    controle_validade_pro = models.CharField('Controle de validade',max_length=1,null=True,blank=True)
    naocorautomatico_pro = models.CharField('Não cor automático',max_length=1,null=True,blank=True)
    foto1_pro = models.ImageField('Foto',upload_to='produtos/',null=True,blank=True,default='produtos/foto.jpg')
#    foto2_pro = StdImageField('Foto 2',upload_to=get_file_path,variations={'thumb':(225,225)},null=True,blank=True)
#    foto3_pro = StdImageField('Foto 3',upload_to=get_file_path,variations={'thumb':(225,225)},null=True,blank=True)
#    foto4_pro = StdImageField('Foto 4',upload_to=get_file_path,variations={'thumb':(225,225)},null=True,blank=True)
#    foto5_pro = StdImageField('Foto 5',upload_to=get_file_path,variations={'thumb':(225,225)},null=True,blank=True)
#    foto6_pro = StdImageField('Foto 6',upload_to=get_file_path,variations={'thumb':(225,225)},null=True,blank=True)
    mercadolivre_pro = models.CharField('Mercado livre',max_length=1,null=True,blank=True)
    teste = models.BinaryField('byres de teste ', null =True , blank= True)
    

    class Meta:
        ordering = ['descricao_pro']
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'
    


    #def get_pk(produto_pro:int):
        #return self.produto_pro

    def __str__(self):
        return self.descricao_pro
    #def get_setor(self):
    #   setor =  Setor.objects.all().order_by('pk')
    #    setorpro = SetorPRO.objects.filter(cod_pro_set=pegar,num_setor=setor).values_list(setor.key_tip)
    #    return f ' {setorpro}'
    

    def get_valor(self):
       pegar = self.produto_pro
       user = User.objects.all().order_by('pk')
       valor = self.setor_produto_pro.filter(cod_pro_set=pegar).values_list('preco_venda_set',flat=True)
       return f'{number_format(valor[0],2)}'
    @property
    def get_img_url(Self):
       if self.foto1_pro:
         return self.foto1_pro.url     
       else:
         return "#"
       
        
   # def get_product_url(self):
    #    return f"/produto/{self.produto_pro}"

   # def get_absolute_url(self):
    #    return reverse_lazy(f"/produto/{self.produto_pro}")


class SetorPRO(models.Model):   
    #cod_setorpro = models.AutoField('Codigo sequencial do setor do produto',primary_key=True)
    cod_pro_set = models.ForeignKey(Produto,db_column='cod_pro_set',related_name='setor_produto_pro',verbose_name='codigo do produto no setor',on_delete=models.CASCADE,default=1)
    num_setor = models.ForeignKey('core.Setor',db_column='num_setor',related_name='setor_SETPRO',verbose_name='setor do produto',on_delete=models.CASCADE,default=1)
    qtd_atual = models.DecimalField('Quantidade atual',max_digits=7,decimal_places=2,null=True,blank=True)
    qtd_atual2 = models.DecimalField('Quantidade atual',max_digits=7,decimal_places=2,null=True,blank=True)
    qtd_padrao_set = models.DecimalField('Quantidade Padrao',max_digits=7,decimal_places=2,null=True,blank=True)
    localizacao_set = models.CharField('Localizacao do setor',max_length=13,null=True,blank=True)
    unidade_set = models.CharField('Tipo de unidade',max_length=5,null=True,blank=True)
    fiscal_set = models.CharField('Fiscal',max_length=1,null=True,blank=True)
    preco_venda_set = models.DecimalField('Preço de Venda',max_digits=7,decimal_places=2,null=True,blank=True)
    preco_promocao_set = models.DecimalField('Preço de Promoção',max_digits=7,decimal_places=2,null=True,blank=True)
    barra_fab_set = models.DecimalField('Barra',max_digits=7,decimal_places=2,null=True,blank=True)
    peso_fin_set = models.DecimalField('Peso',max_digits=7,decimal_places=2,null=True,blank=True)
    qtd_antecipada = models.DecimalField('Quantidade antecipada',max_digits=7,decimal_places=2,null=True,blank=True)
    qtd_minima_set= models.DecimalField('Quantidade minima',max_digits=7,decimal_places=2,null=True,blank=True)
    ult_datahora_set = models.DateTimeField('Data hora ultima alteracao',null=True,blank=True,default=timezone.now)
    tipo_comis_vend_set = models.CharField('Tipo comissao vendedor',max_length=1,null=True,blank=True)
    tipo_comis_pres_set = models.CharField('Tipo comissao prestador',max_length=1,null=True,blank=True)
    comis_vend_set = models.DecimalField('Comissao vendedor',max_digits=7,decimal_places=2,null=True,blank=True)
    comis_pres_set = models.DecimalField('Comissao prestador',max_digits=7,decimal_places=2,null=True,blank=True)
    ult_custo_set= models.DecimalField('Ultimo custo',max_digits=7,decimal_places=2,null=True,blank=True)
    ult_invent_fis_set = models.DateTimeField('Ultima fiscal',null=True,blank=True,default=timezone.now)

    class Meta:
        ordering = ['cod_pro_set']
        verbose_name = 'setorpro'
        verbose_name_plural = 'setorespro'
    def get_product_url(self):
        chave = Produto.objects.filter(self.cod_pro_set).values_list(produto_pro)
        return f"/produto/{chave}/"
    
    def get_absolute_url(self):
         chave = Produto.objects.filter(self.cod_pro_set).values_list(produto_pro)

         return reverse_lazy(f"/produto/{chave}")

    

    def __str__(self):
        return self.cod_pro_set.descricao_pro
    def get_img(self):
        if foto1_pro == None:
            return f'../../../static/img/Entrada SIG-2000.JPG'
        else :
           return self.foto1_pro
    def get_valor(self):
        if  self.preco_venda_set == None:
            self.preco_venda_set = 0
            self.preco_venda_set = float(self.preco_venda_set)
            return f'R${number_format(self.preco_venda_set,2)}'
        else:
             if  self.preco_venda_set > 0: 
          #      breakpoint()    
                self.preco_venda_set = float(self.preco_venda_set)
    
                return f'R$ {number_format(self.preco_venda_set,2)}'

#modificado  para os parametros da table de base , Davi Oliveira Tito 11/05/2022
class TipoPRO(models.Model):
    cod_tip_pro = models.AutoField('ID',primary_key=True,serialize=False)
    key_tip = models.CharField('Chave',max_length=3,null=False,blank=True)
    desc_tip = models.CharField('Descrição do tipo',max_length=300,null=True,blank=True)
    desconto_max_tip = models.DecimalField('Desconto máximo do tipo',max_digits=7,decimal_places=2,null=True,blank=True)
    transmitido = models.CharField('Transmitido',max_length=3,null=True,blank=True,choices = loja_virt_list)
    #Modificadado Davi Oliveira Tito 
    mostrar_msg_tip = models.CharField('Mostrar mensagem',max_length=3,null=True,blank=True)
  # cod_usu_alt  = models.IntegerField('Codigo do Usuar', blank = True  , null = True)
  #  data_mod = models.DateTimeField('Data da ultima alteracao',editable=False,default=datetime.date.today())
  #  data_mod = models.DateTimeField('Data da ultima alteracao',editable=False,default=timezone.now)
    def __str__(self):
       # return self.id_tipopro
        return self.key_tip
# modificado Davi Oliveira tito, mudado key_tip.desc_tip, para somente key_tip 17/05/2022
#modificado, retirado retrun self.key_tip 17/05/2022 Davi Oliveira Tito
#teste equivocado return self.id_tipopro, 17/05/2022 Davi Oliveira Tito
#adição de get_tiproduct_url e get_absolute_url
    class Meta:
        # ordering modificado de key_tip para id_tipopro DAvi Oliveira Tito 17/05/2022
        ordering = ['cod_tip_pro']
        verbose_name = 'Tipo do produto'
        verbose_name_plural="tipos dos produtos"
   # def get_product_url(self):
    #    return f"/tipopro/{self.key_tip}"

    def get_absolute_url(self):
        return reverse_lazy(f"/tipopro{self.key_tip}")

#Modificado 27/05/2022 Davi O.Tito
class GrupoPRO(models.Model):
    codigo_gru = models.AutoField('ID',primary_key=True)
    desc_gru = models.CharField('Nome do grupo',max_length=60,null=True,blank=True)
    cod_interligacao_gru = models.IntegerField('Tipo de Desconto',null=True,blank=True)
    ult_usuario_gru = models.CharField('Usuario ultima alteracao',max_length=15,null=True,blank=True,editable=False,default=User)
  #  ult_data_gru = models.DateTimeField('Data ultima alteracao',null=True,blank=True,default=timezone.now)
  #  ult_hora_gru = models.DateTimeField('Hora ultima alteracao',null=True,blank=True,default=timezone.now)
    transmitido_gru = models.CharField('Transmitido',max_length=1,null=True,blank=True) 
    tipo_desconto_gru = models.CharField('Tipo de desconto',max_length=1,null=True,blank=True) 
    lojavirt_gru = models.CharField('Loja Virtual',max_length=3,null=True,blank=True,choices = loja_virt_list)
    garantia_mercadolivre_gru = models.CharField('Garantia Mercado Livre',max_length=60,null=True,blank=True)
    categoria_mercadolivre_gru = models.CharField('Categoria Mercado Livre',max_length=60,null=True,blank=True)
    
    class Meta:
        ordering = ['codigo_gru']
        verbose_name = 'Grupo do produto'

    def __str__(self):
        return self.desc_gru
#adicionado cupom, Davi Oliveira Tito 10/05/2022
class cupom(models.Model):
    id_cupom = models.AutoField('ID',primary_key=True)
    valor_cupom = models.DecimalField('valor do  cupom',max_digits=5,decimal_places=2,help_text="valor de desconto do cupom")
    nome_cupom = models.CharField('Descricao do cupom',max_length=300,null=True)
    setor_do_pro = models.IntegerField('codigo do setor do cupo',null=True)
    cod_usu_alt = models.ForeignKey('users.User',null=True,db_column='cod_usu_alt',related_name='cod_users_user',on_delete=models.CASCADE)
    data_inic = models.DateTimeField('Data do inicio',editable=False,default=timezone.now)
    data_fim = models.DateTimeField('Data do fim',default=timezone.now)
    class Meta:
        ordering = ['id_cupom']
        verbose_name ='Cupons de desconto'
#adicionado Unidade, Davi 26/05/2022
class Unidade(models.Model):
    id_uni = models.AutoField('ID',primary_key=True)
    unidade_uni= models.CharField('codigo da unidade',null=False,blank=True,max_length=2)
    descricao_uni = models.CharField('Descricao do cupom',max_length=300,null=True)
    sigla_uni = models.CharField('sigla da unidade',null=True,max_length=2)
    un_tiss_uni= models.IntegerField('tss',null=True,blank=True)
    class Meta:
        ordering = ['id_uni']
        verbose_name ='Unidades'

    def __str__(self): 
        return self.descricao_uni
class NCM_CEST(models.Model):
    NCM_cabec = models.CharField('cabeçalho',max_length=20,null=True,blank=True,editable=False)
    codigo_ncm_sh = models.DecimalField('codigo NCM/SH',primary_key=True,max_digits=8,decimal_places=0,null=False,blank=True,help_text="NOMECLATURA COMUM DO MERCO SUL")
    codigo_Cest = models.DecimalField('codigo Cest', null =False ,max_digits=8,decimal_places=0,blank=True,help_text="Codigo Especificador da Substituição TributariaS")
    descricao_cest = models.TextField('descricao cest', null = True, blank=True ,help_text="Descricao do  NCM/CEXT do produto de Substituição tributaria")
    Ncm_calc_pob =  models.BooleanField('calcula fundo de combate a pobresa ', default=False ,help_text="somente calcula se for consumidor para fora do estado") 
    MVa_original = models.DecimalField('MVN_ORIGINAL',max_digits=7,decimal_places=2,default=1,null=True,blank=True,help_text="QUal a porcentagem de MVA ORiginal para calculo de substituição tributaria(somente venda no atacado)")
    class Meta:
        ordering = ['NCM_cabec']
        verbose_name='manutencao da tabela ncm/cest'




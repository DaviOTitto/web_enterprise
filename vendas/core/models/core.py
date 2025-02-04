import uuid
import re
from django.db import models
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, resolve_url, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.utils.formats import number_format
from django.utils import timezone
from vendas.users.models import User

from ..models import *
from datetime import datetime
gender_list = [('M', 'Masculino'), ('F', 'Feminino')]

class TimeStampedModel(models.Model):
    created = models.DateTimeField('criado em', auto_now_add=True, auto_now=False,default=timezone.now)
    modified = models.DateTimeField('modificado em', auto_now_add=False, auto_now=True,default=timezone.now)

    class Meta:
        abstract = True

# Para gerar nomes únicos de arquivos de imagem
def get_file_path(_instance, filename): 
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename


class CondPag(models.Model):
    codigo = models.AutoField('Código',primary_key=True)
    descricao = models.CharField("Descrição",max_length=40,null=True,blank=True)
    juros = models.DecimalField('Juros',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    tipo_juros = models.CharField("Tipo juros",max_length=1,null=True,blank=True)
    pri_dias_prazo = models.IntegerField('Primeiro dia prazo',null=True,blank=True)
    seg_dias_prazo = models.IntegerField('Segundo dia prazo',null=True,blank=True)
    ter_dias_prazo = models.IntegerField('Terceiro dia prazo',null=True,blank=True)
    qua_dias_prazo = models.IntegerField('Quarto dia prazo',null=True,blank=True)
    qui_dias_prazo = models.IntegerField('Quinto dia prazo',null=True,blank=True)
    sex_dias_prazo = models.IntegerField('Sexto dia prazo',null=True,blank=True)
    imp_cupom = models.CharField("Imprime cupom",max_length=1,null=True,blank=True)
    cota_vend = models.DecimalField('Cota',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    comissao_1_vend = models.DecimalField('Comissão 1',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    comissao_2_vend = models.DecimalField('Comissão 2',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    demais_dias_prazo = models.IntegerField('Demais dia prazo',null=True,blank=True)
    conta_bancaria = models.IntegerField('Conta bancária',null=True,blank=True)
    especie_doc = models.CharField("Espécie documento",max_length=2,null=True,blank=True)
    num_parcelas = models.IntegerField('Número parcelas',null=True,blank=True)
    utilizacao = models.CharField("Utilização",max_length=1,null=True,blank=True)
    contagem_dias = models.CharField("Contagem dias",max_length=1,null=True,blank=True)
    dia_fixo_venc = models.IntegerField('Dia fixo',null=True,blank=True)
    cod_financeira = models.IntegerField('Condição financeira',null=True,blank=True)
    desc_financiamento = models.DecimalField('Desconto financiamento',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    obriga_cli_condpag = models.CharField("Obriga cliente",max_length=1,null=True,blank=True)
    trasmitido = models.CharField("Transmitido",max_length=1,null=True,blank=True)
    nao_baixa_par_condpag = models.CharField("Não baixar parametro",max_length=1,null=True,blank=True)
    aceitaespvazia_condpag = models.CharField("Aceita espécie vazia",max_length=1,null=True,blank=True)
    nao_imp_condpag = models.CharField("Não imprime",max_length=1,null=True,blank=True)
    prazo_max_diascondpag = models.IntegerField('Prazo máximo dias',null=True,blank=True)
    taxa_financeiracondpag = models.DecimalField('Taxa financeira',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    entrada_avistacondpag = models.CharField("Entrada a vista",max_length=1,null=True,blank=True)
    entradacondpag = models.DecimalField('Entrada',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    nao_aceitar_desc = models.CharField("Não aceitar desconto",max_length=1,null=True,blank=True)

    class Meta:
        ordering = ['descricao']
        verbose_name = 'Forma de pagamento'
        verbose_name_plural = 'Formas de pagamento'

    def __str__(self):
        return str(self.descricao)


class Especie(models.Model):
    sigla_esp = models.CharField("Sigla",max_length=2,primary_key=True)
    descricao_esp = models.CharField("Descrição",max_length=30,null=True,blank=True)
    abreviatura_esp = models.CharField("Abreviatura",max_length=15,null=True,blank=True)
    nao_move_banco_esp = models.CharField("Não move banco",max_length=1,null=True,blank=True)

    class Meta:
        verbose_name = 'Condição de pagamento'
        verbose_name_plural = 'Condições de pagamento'

class Venda(models.Model):
    numero_ven = models.AutoField('Número sequencial da venda',primary_key=True)
    data_ven = models.DateTimeField('Data e hora da venda',auto_now_add=True,auto_now=False)
    nf_ven = models.IntegerField('NF',null=True,blank=True)
    cliente_ven = models.ForeignKey('core.Cadastro',db_column='cliente_ven',related_name='cadastros_sale',on_delete=models.CASCADE)
    formapag_ven = models.ForeignKey(CondPag,db_column='formapag_ven',related_name='forma_pag',on_delete=models.CASCADE)
    usuario_ven = models.ForeignKey('users.User',db_column='usuario_ven',related_name='usuario_sale',on_delete=models.CASCADE)
    desconto_ven = models.DecimalField('Desconto',max_digits=7,decimal_places=2,null=True,blank=True)
    condicao_ven = models.IntegerField('Condição',null=True,blank=True)
    obs_ven = models.TextField('Observações',blank=True,null=True)
    frete = models.DecimalField('Frete',max_digits=7,decimal_places=2,null=True,blank=True)
    seguro = models.DecimalField('Seguro',max_digits=7,decimal_places=2,null=True,blank=True)
    despesas_acess = models.DecimalField('Despesas acessórias',max_digits=7,decimal_places=2,null=True,blank=True)
    codigo_transport = models.IntegerField('Código Transporte',null=True,blank=True)
    placa_veic = models.CharField('Placa veículo',max_length=10,null=True,blank=True)
    uf_veic = models.CharField('UF veículo',max_length=2,null=True,blank=True)
    frete_por_conta = models.CharField('Frete por conta',max_length=1,null=True,blank=True)
    marca = models.CharField('Marca',max_length=10,null=True,blank=True)
    especie = models.CharField('Espécie',max_length=10,null=True,blank=True)
    numeracao = models.CharField('Numeração',max_length=10,null=True,blank=True)
    prev_entrega  = models.DateTimeField('Data e hora da previsão de entrega',null = True,auto_now_add=True,auto_now=False)
    setor_ven = models.IntegerField('Setor',null=True,blank=True)
    precosetor_ven = models.IntegerField('Preço setor',null=True,blank=True)
    datanfsai_ven  = models.DateTimeField('Data e hora da Nota Fiscal',null = True,auto_now_add=True,auto_now=False)
    horanfsai_ven  = models.DateTimeField('Data e hora da Nota Fiscal',null = True,auto_now_add=True,auto_now=False)
    imprime_romaneio_ven = models.CharField('Imprime romaneio',max_length=1,null=True,blank=True)
    cupom_impresso_ven = models.CharField('Cumpom Impresso',max_length=1,null=True,blank=True)
    prestador_serv_ven = models.IntegerField('Prestador serviço',null=True,blank=True)
    usuario_atu_ven = models.IntegerField('Usuário atual',null=True,blank=True)
    data_atu_ven  = models.DateTimeField('Data e hora da atualização da venda',auto_now_add=True,auto_now=False,null=True)
    hora_atu_ven  = models.DateTimeField('Data e hora da atualização da venda',auto_now_add=True,auto_now=False,null=True)
    cupom_ven = models.IntegerField('Cupom',null=True,blank=True)
    qtd_vol_ven = models.IntegerField('Quantidade volume',null=True,blank=True)
    num_venda_antecip_ven = models.IntegerField('Número venda antecipada',null=True,blank=True)
    usuarioinc_ven = models.IntegerField('Usuário inclusão',null=True,blank=True)
    datainc_ven  = models.DateTimeField('Data e hora da inclusão da venda',auto_now_add=True,auto_now=False,null = True)
    serieimp_ven = models.CharField('Serie IMP',max_length=20,null=True,blank=True)
    sequencimp_ven = models.DecimalField('Sequência IMP',max_digits=7,decimal_places=2,null=True,blank=True)
    num_empenho_ven = models.IntegerField('Número empenho',null=True,blank=True)
    dat_empenho_ven = models.DateTimeField('Data e hora do empenho',auto_now_add=True,auto_now=False,null=True)
    cod_unid_exec_ven = models.CharField('Código Unidade Executivo',max_length=10,null=True,blank=True)
    sit_ven = models.CharField('Situação',max_length=30,null=True,blank=True)
    ult_usu_lib_ven = models.IntegerField('Último usuário lib',null=True,blank=True)
    ult_datahora_lib_ven = models.DateTimeField('Última data e hora lib',auto_now_add=True,auto_now=False,null = True)
    status_imp_ven = models.CharField('Status IMP',max_length=1,null=True,blank=True)
    km = models.DecimalField('KM',max_digits=7,decimal_places=2,null=True,blank=True)
    acrescimo_ven = models.DecimalField('Acréscimo',max_digits=7,decimal_places=2,null=True,blank=True)
    frete_entra_finan_ven = models.CharField('Frete entrada',max_length=1,null=True,blank=True)
    seguro_entra_finan_ven = models.CharField('Seguro entrada',max_length=1,null=True,blank=True)
    desp_acess_entra_finan_ven = models.CharField('Despesas acessórias entrada',max_length=1,null=True,blank=True)
    hora_ven = models.DateTimeField('Hora da venda',null = True,auto_now_add=True,auto_now=False)
    romaneio_comis = models.CharField('Romaneio comissão',max_length=1,null=True,blank=True)
    serie_nf_ven = models.IntegerField('Série NF',null=True,blank=True)
    nome_xml_nfe_ven = models.CharField('Nome XML NFe',max_length=60,null=True,blank=True)
    chave_acesso_nfe_ven = models.CharField('Chave de acesso NFe',max_length=60,null=True,blank=True)
    protocolo_nfe_ven = models.CharField('Protocolo NFe',max_length=50,null=True,blank=True)
    tipo_entrega_ven = models.CharField('Tipo de entrega',max_length=20,null=True,blank=True)
    protocolo_cancela_ven = models.CharField('Protocolo Cancelamento',max_length=20,null=True,blank=True)
    retimp_ven = models.CharField('RET IMP',max_length=10,null=True,blank=True)
    irimp_ven = models.CharField('IR IMP',max_length=10,null=True,blank=True)
    parcelar_serv = models.CharField('Parcelar serviço',max_length=1,null=True,blank=True)
    tot_servicos = models.DecimalField('Total serviços',max_digits=7,decimal_places=2,null=True,blank=True)
    tot_pecas = models.DecimalField('Total peças',max_digits=7,decimal_places=2,null=True,blank=True)
    importado_cf_ven = models.CharField('Importador',max_length=1,null=True,blank=True)
    cod_vend_comiss_ven = models.IntegerField('Código vendedor comissão',null=True,blank=True)
    irrf_ven = models.DecimalField('IRRF',max_digits=7,decimal_places=2,null=True,blank=True)
    pis_ven = models.DecimalField('PIS',max_digits=7,decimal_places=2,null=True,blank=True)
    cofins_ven = models.DecimalField('COFINS',max_digits=7,decimal_places=2,null=True,blank=True)
    csll_ven = models.DecimalField('CSLL',max_digits=7,decimal_places=2,null=True,blank=True)
    issqn_apagar_ven = models.DecimalField('ISSQN A pagar',max_digits=7,decimal_places=2,null=True,blank=True)
    issqn_retido_ven = models.DecimalField('ISSQN Retido',max_digits=7,decimal_places=2,null=True,blank=True)
    inss_ven = models.DecimalField('INSS',max_digits=7,decimal_places=2,null=True,blank=True)
    modelo_nf_ven = models.CharField('Modelo NF',max_length=3,null=True,blank=True)
    transformou_nfe_sem_entrada = models.CharField('Transformou em NFe Sem Entrada',max_length=1,null=True,blank=True)
    valor_entrega_ven = models.DecimalField('Valor Entrega',max_digits=7,decimal_places=2,null=True,blank=True)

    class Meta:
        verbose_name = 'venda'
        verbose_name_plural = 'vendas'        
   # comentado para testes, lembrar remover '#' Davi 08/7     
   #problemas nesta linha 04/07/2022, Davi, PS: problema parcialmente resolvido :)
    # modificado Davi 05/07/2022
   # def __str__(self):
        #return f'{self.numero_ven:03d}/%s' 
    #codigo = property(__str__)
   # voltei ao original 10/07/2022 Davi Oliveira Tito
   # def __str__(self):
    #   return f'{self.numero_ven:03d}/%s' % self.data_ven.strftime("%Y")  
   # codigo = property(__str__)
   # def __str__(self):
   #    return f'{self.numero_ven}/%s' % self.data_ven.strftime("%Y")  
   # codigo = property(__str__)

    def get_absolute_url(self):
        return reverse_lazy('core:venda_det', pk=self.numero_ven)

    def get_data_ven(self):
        #self.data_ven=time.today()
        return self.data_ven.strftime("%d/%m/%Y")

    def get_hora_ven(self):
        self.hora_ven=datetime.today()
        return self.hora_ven.strftime("%H:%M:%S")
        
    def get_detalhe(self):
        return f'/venda/{self.numero_ven}'

    # conta os itens em cada venda
    def get_itens(self):
        return self.vendas_det.count()
    #alteração feita em get_Desconto,porem retornadoDavi Oliveira tito 04/05/2022
   
    def get_desconto(self):
       # self.desconto_ven= float(self.desconto_ven)
        #breakpoint()
        print(self.desconto_ven)
        if  self.desconto_ven == None:
            self.desconto_ven = 0
            self.desconto_ven = float(self.desconto_ven)
            return f'R${number_format(self.desconto_ven,2)}'
        else:
            if  self.desconto_ven > 0: 
          #      breakpoint()    
                self.desconto_ven = float(self.desconto_ven)
    
                return f'R$ {number_format(self.desconto_ven,2)}'
            else :
                
                self.desconto_ven = float(self.desconto_ven)
                return f'R$ {number_format(self.desconto_ven,2)}'
    #modificado dia 07/07/2022 , Nome Davi Oliveira Tito
    def get_total(self):
        # recupera desconto e atribui 0 se não existir
        desc = Venda.objects.filter(numero_ven=self.numero_ven).values_list('desconto_ven') or 0
        d = float
        d = 0 if None in desc[0] else float(sum(map(lambda d: d[0], desc)))
        # recupera itens da venda e atribui 0 se não existir
        qs = self.vendas_det.filter(num_ven_ite=self.numero_ven).values_list(
            'unitario_ite', 'quantidade_ite') or 0
        t = 0 if isinstance(qs, int) else float(sum(map(lambda q: q[0] * q[1] , qs)))-d
        
        return f'R$ {number_format(t, 2)}'
   # def get_total(self):
        # recupera desconto e atribui 0 se não existir
      #  desc = Venda.objects.filter(numero_ven=self.numero_ven).values_list('desconto_ven') or 0
      #  d = float(0)
      #  if None in desc:
      #      d= float(0) 
       # else: 
        #    sum(map(lambda d: d[0], desc))
        # recupera itens da venda e atribui 0 se não existir
      #  qs = self.vendas_det.filter(num_ven_ite=self.numero_ven).values_list(
       #     'unitario_ite', 'quantidade_ite') or 0
       # t = 0 if isinstance(qs, int) else float(sum(map(lambda q: (q[0] * q[1])-d, qs)))  
      #  return f'R$ {number_format(t, 2)}'


        
    
    #def get_total(self):
       # # recupera desconto e atribui 0 se não existir
       # desc = Venda.objects.filter(numero_ven=self.numero_ven).values_list('desconto_ven') or 0
        #d = 0 if None in desc else sum(map(lambda d: d, desc))
       # # recupera itens da venda e atribui 0 se não existir
       # qs = self.vendas_det.filter(num_ven_ite=self.numero_ven).values_list(
       #     'unitario_ite', 'quantidade_ite') or 0
       # t = 0 if isinstance(qs, int) else float(sum(map(lambda q: q[0] * q[1], qs))) - d
        
       # return f'R$ {number_format(t, 2)}'

        
       # return f'R$ {number_format(t, 2)}'
   
    #def get_total(self):
      #  # recupera desconto e atribui 0 se não existir
      #  desc = float#
      #  desc = Venda.objects.filter(numero_ven=self.numero_ven).values_list('desconto_ven') or 0             
       # desc = Venda.objects.filter(numero_ven=self.numero_ven).values_list('desconto_ven') or 0
      
      #  d = 0 if None in desc[0] else sum(map(lambda d: d[0], desc))
        # recupera itens da venda e atribui 0 se não existir
     #   qs = self.vendas_det.filter(num_ven_ite=self.numero_ven).values_list(
     #       'unitario_ite', 'quantidade_ite') or 0
     #   t = 0 if isinstance(qs, int) else float(sum(map(lambda q: q[0] * q[1], qs))) - d
        F
     #   return f'R$ {number_format(t, 2)}'


class ItemVEN(models.Model):
    cod_itemven = models.AutoField('Código',primary_key=True)
    num_ven_ite = models.ForeignKey(Venda,db_column='num_ven_ite',related_name='vendas_det',on_delete=models.CASCADE)    
    produto_ite = models.ForeignKey('core.Produto',db_column='produto_ite',related_name='produto_det',on_delete=models.CASCADE)
    quantidade_ite = models.DecimalField('Quantidade', max_digits=7,decimal_places=0,default=1)
    unitario_ite = models.DecimalField('Valor unitário',max_digits=7,default=1,decimal_places=2)
    ipi_ite = models.DecimalField('IPI',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    comispro_ite = models.DecimalField('Comissão produto',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    val_tot_contabil_ite = models.DecimalField('Valor total contábil',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    val_ipi_contabil_ite = models.DecimalField('Valor IPI contábil',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    val_base_icms_ite = models.DecimalField('Valor base ICMS',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    quant_dev_ite = models.DecimalField('Quantidade devolvida',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    nf_ven_ite = models.IntegerField('Nota Fiscal venda',null=True,blank=True)
    sigla_fab_pro_ite = models.CharField('Sigla Fabricação produto',max_length=15,null=True,blank=True)
    farmaciapop_posologia_ite = models.DecimalField('Farmácia posologia',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    farmaciapop_qtdsolic_ite = models.DecimalField('Farmácia quantidade solicitada',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    bico_ite = models.IntegerField('Bico',null=True,blank=True)
    aliq_icms_ite = models.DecimalField('Alíquota ICMS',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    sit_trib_ite = models.IntegerField('Situação tributária',null=True,blank=True)
    base_calc_st_ite = models.DecimalField('Base cálculo ST',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    valor_st_ite = models.DecimalField('Valor ST',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    cfo_ite = models.IntegerField('CFO',null=True,blank=True)
    seq_digita_itemven = models.IntegerField('Sequência digita',null=True,blank=True)
    xped = models.DecimalField('XPED',max_digits=7,decimal_places=2,default=1,null=True,blank=True)
    nitemped = models.IntegerField('Nitemped',null=True,blank=True)

    def __str__(self):
        return str(self.num_ven_ite)

    def get_unitario_ite(self):          

        setorPro = SetorPRO.objects.filter(
            num_setor=self.num_ven_ite.setor_ven, 
            cod_pro_set = self.produto_ite.produto_pro).values_list('preco_venda_set').get
        print('produto')
        print(self.produto_ite.produto_pro)
        print('setor')
        print(self.num_ven_ite.setor_ven)
        t = float(setorPro)
        print(t[0])
        return f'R$ {number_format(self.t,2)}'
    

    def get_subtotal(self):
        return self.unitario_ite * (self.quantidade_ite or 0)

    subtotal = property(get_subtotal)

    def getID(self):
        return f"{self.id:04d}"

    def price_sale_formated(self):
        return "R$ %s" % number_format(self.unitario_ite, 2)

    def subtotal_formated(self):
        return "R$ %s" % number_format(self.subtotal, 2)
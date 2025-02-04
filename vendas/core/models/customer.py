 import uuid
import re
from django.db import models
from stdimage.models import StdImageField
from django.utils import timezone
from pathlib import Path, os
# Para gerar nomes únicos de arquivos de imagem
def get_file_path(_instance, filename): 
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename


class Setor(models.Model):
    key_setor = models.AutoField('Código setor',primary_key=True)
    desc_setor = models.CharField('Descrição setor',max_length=20)
    cadastro_setor = models.IntegerField('Cadastro',null=True,blank=True)
    destino_setor = models.IntegerField('Destino',null=True,blank=True)
    sep_setor = models.CharField('Sep setor',max_length=1,null=True,blank=True)
    destcc_setor = models.IntegerField('Destcc',null=True,blank=True)
    ccag_setor = models.IntegerField('CCAG',null=True,blank=True)
    agrup_contas_setor = models.CharField('Agrupar contas setor',max_length=1,null=True,blank=True)
    usu_alt_setor = models.IntegerField('Usuário alteração',null=True,blank=True)
    data_alt_setor = models.DateTimeField('Data alteração',null=True,blank=True,default=timezone.now)
    comisgerente_geral_setor = models.DecimalField('Comissão gerente geral',max_digits=7,decimal_places=2,null=True,blank=True)
    comisgerente_local_setor = models.DecimalField('Comissão gerente local',max_digits=7,decimal_places=2,null=True,blank=True)
    area_comercial_setor = models.CharField('Área comercial setor',max_length=1,null=True,blank=True)
    area_servico_setor = models.CharField('Área serviço setor',max_length=1,null=True,blank=True)
    area_industria_setor = models.CharField('Área industria setor',max_length=1,null=True,blank=True)
    taxa_iss_setor = models.DecimalField('Taxa ISS',max_digits=7,decimal_places=2,null=True,blank=True)
    cod_emp_para_nfe_setor = models.IntegerField('Código empresa para NFe',null=True,blank=True)
    taxa_inss_setor = models.DecimalField('Taxa INSS',max_digits=7,decimal_places=2,null=True,blank=True)
    taxa_csll_setor = models.DecimalField('Taxa CSLL',max_digits=7,decimal_places=2,null=True,blank=True)
    mapa_set = models.CharField('Mapa setor',max_length=10,null=True,blank=True)
    cod_gerente_setor = models.IntegerField('Código gerente',null=True,blank=True)
    cod_resp_tecnico_setor = models.IntegerField('Código responsável técnico',null=True,blank=True)
    numserie_cert_prod_setor = models.CharField('Número série cert produto',max_length=60,null=True,blank=True)
    numserie_cert_serv_setor = models.CharField('Número série cert serviço',max_length=60,null=True,blank=True)
    sem_capicom_setor = models.CharField('Sem campicom',max_length=1,null=True,blank=True)
    caminho_certificado_setor = models.CharField('Caminho certificado',max_length=100,null=True,blank=True)
    senha_certificado_setor = models.CharField('Senha certificado',max_length=30,null=True,blank=True)
    conta_bancaria_setor = models.IntegerField('Conta bancária',null=True,blank=True)
    csc_setor = models.CharField('CSC',max_length=32,null=True,blank=True)
    timeout_nf_setor = models.IntegerField('Timeout NF',null=True,blank=True)
    ajusta_aut_aguardar_nf_setor = models.CharField('Ajusta automático aguardar NF',max_length=1,null=True,blank=True)
    aguardar_nf_setor = models.IntegerField('Aguardar NF',null=True,blank=True)
    num_tentativa_nf_setor = models.IntegerField('Número de tentativas NF',null=True,blank=True)
    intervalo_nf_setor = models.IntegerField('Intervalo NF',null=True,blank=True)       
    devolucao_ven_setor = models.CharField('Devolução venda',max_length=1,null=True,blank=True)
    dat_ult_trans_conting_setor = models.DateTimeField('Data última transmissão contingência',null=True,blank=True,default=timezone.now)
    tempo_paraverif_trans_setor = models.IntegerField('Tempo verificação transmissão',null=True,blank=True)
    token_ibpt_setor = models.CharField('Token ibpt',max_length=100,null=True,blank=True)
    simples_minas_setor = models.CharField('Simples minas',max_length=1,null=True,blank=True)
    simples_nacional_setor = models.CharField('Simples nacional',max_length=1,null=True,blank=True)
    simples_nacional_serv_setor = models.CharField('Simples nacional serviço',max_length=1,null=True,blank=True)       
    class Meta:
        ordering = ['key_setor']
        verbose_name = 'Setore'

        

    def __str__(self):
        return self.desc_setor

    def get_setor_url(self):
        return f"/setor/{self.key_setor}"

    # retorna as vendas do setor
    def get_sale_setor_url(self):
        return f'/venda/?setor_sale={self.key_setor}'

    # número de vendas por setor
    def get_sales_count(self):
        return self.setor_sale.count()


class Customer(models.Model):
    codigo_cad = models.AutoField('Código do Cadastro',primary_key=True)
    registro_cad = models.CharField('Registro do Cadastro',max_length=20,null=True,blank=True)
    nome_cad = models.CharField('Nome',max_length=60,null=True,blank=True)
    rua1_cad = models.CharField('Rua',max_length=40,null=True,blank=True)
    bairro1_cad = models.CharField('Bairro',max_length=20,null=True,blank=True)
    cidade1_cad = models.CharField('Cidade',max_length=30,null=True,blank=True)
    rua2_cod = models.CharField('Rua 2',max_length=40,null=True,blank=True)
    bairro2_cad = models.CharField('Bairro 2',max_length=20,null=True,blank=True)
    cidade2_cad = models.CharField('Cidade 2',max_length=30,null=True,blank=True)
    razao_cad = models.CharField('Razão',max_length=60,null=True,blank=True)
    contato_cad = models.CharField('Contato',max_length=40,null=True,blank=True)
    cgc_cpf_cad = models.CharField('CGC - CPF',max_length=20,null=True,blank=True)
    ie_cad = models.CharField('Inscrição estadual',max_length=20,null=True,blank=True)
    aniversario_cad = models.DateTimeField('Aniversário',null=True,blank=True,default=timezone.now)
    classe_cli_cad = models.CharField('Classe cliente',max_length=3,null=True,blank=True)
    classe_for_cad = models.CharField('Classe fornecedor',max_length=3,null=True,blank=True)
    classe_des_cad = models.CharField('Classe des',max_length=3,null=True,blank=True)
    classe_rec_cad = models.CharField('Classe rec',max_length=3,null=True,blank=True)
    cep1_cad = models.CharField('CEP',max_length=9,null=True,blank=True)
    estado1_cad = models.CharField('Estado',max_length=2,null=True,blank=True)
    cep2_cad = models.CharField('CEP 2',max_length=9,null=True,blank=True)
    estado2_cad = models.CharField('Estado 2',max_length=2,null=True,blank=True)
    telefone1_cad = models.CharField('Telefone',max_length=15,null=True,blank=True)
    telefone2_cad = models.CharField('Telefone 2',max_length=15,null=True,blank=True)
    fax_cad = models.CharField('Fax',max_length=15,null=True,blank=True)
    ult_data_cad = models.DateTimeField('Última data',null=True,blank=True,default=timezone.now)
    prim_data_cad = models.DateTimeField('Primeira data',null=True,blank=True,default=timezone.now)
    prox_data_cad = models.DateTimeField('Próxima data',null=True,blank=True,default=timezone.now)
    cobranca_cad = models.CharField('Cobrança',max_length=1,null=True,blank=True)
    indice1_cad  = models.DecimalField('Índice 1',max_digits=7,decimal_places=2,null=True,blank=True)
    indice2_cad = models.DecimalField('Índice 2',max_digits=7,decimal_places=2,null=True,blank=True)
    interligacao_cad = models.IntegerField('Interligação',null=True,blank=True)
    filiacao_cad = models.CharField('Filiação',max_length=50,null=True,blank=True)
    data_cadas_cad = models.DateTimeField('Data cadastro',null=True,blank=True,default=timezone.now)
    est_civ_cad = models.CharField('Estado civil',max_length=1,null=True,blank=True)
    observacao_cad = models.TextField('Observação',blank=True,null=True)
    #foto_cad = StdImageField('Foto',upload_to=get_file_path,variations={'thumb':(225,225)},null=True,blank=True)
    sexo_cad = models.CharField('Sexo',max_length=1,null=True,blank=True)
    classe_5_cad = models.CharField('Classe 5',max_length=3,null=True,blank=True)
    classe_6_cad = models.CharField('Classe 6',max_length=3,null=True,blank=True)
    classe_7_cad = models.CharField('Classe 7',max_length=3,null=True,blank=True)
    classe_8_cad = models.CharField('Classe 8',max_length=3,null=True,blank=True)
    classe_9_cad = models.CharField('Classe 9',max_length=3,null=True,blank=True)
    classe_10_cad = models.CharField('Classe 10',max_length=3,null=True,blank=True)
    mala_direta_cad = models.CharField('Mala direta',max_length=1,null=True,blank=True)
    usuario_cad = models.IntegerField('Usuário',null=True,blank=True)
    data_cad  = models.DateTimeField('Data cad',null=True,blank=True,default=timezone.now)
    hora_cad  = models.DateTimeField('Hora cad',null=True,blank=True,default=timezone.now)
    cor_cad = models.CharField('Cor',max_length=1,null=True,blank=True)
    turma_cad = models.IntegerField('Turma',null=True,blank=True)
    nome_pai_cad = models.CharField('Nome do pai',max_length=40,null=True,blank=True)
    profissao_pai_cad = models.CharField('Profissão pai',max_length=30,null=True,blank=True)
    profissao_mae_cad = models.CharField('Profissão mãe',max_length=30,null=True,blank=True)
    religiao_cad = models.CharField('Religião',max_length=2,null=True,blank=True)
    dia_pagamento_cad = models.IntegerField('Dia de pagamento',null=True,blank=True)
    nacionalidade_cad = models.CharField('Nacionalidade',max_length=15,null=True,blank=True)
    registro_nasc_cad = models.CharField('Registro de nascimento',max_length=40,null=True,blank=True)
    naturalidade_cad = models.CharField('Naturalidade',max_length=40,null=True,blank=True)
    interligacao_pdv_cad = models.CharField('Interligação PDV',max_length=15,null=True,blank=True)
    matricula_cad = models.CharField('Matrícula responsável',max_length=40,null=True,blank=True)
    documento_resp_cad = models.CharField('Documento responsável',max_length=40,null=True,blank=True)
    avisos_cad = models.TextField('Avisos',blank=True,null=True)
    motivo_inativo_cad = models.CharField('Motivo inativo',max_length=40,null=True,blank=True)
    data_inativo_cad = models.DateTimeField('Data inativo',null=True,blank=True,default=timezone.now)
    inativo_cad = models.CharField('Inativo',max_length=1,null=True,blank=True)
    segurado_cad = models.CharField('Segurado',max_length=40,null=True,blank=True)
    convenio_cad = models.IntegerField('Convênio',null=True,blank=True)
    indicacao_cad = models.IntegerField('Indicação',null=True,blank=True)
    encaminhamento_cad = models.CharField('Encaminhamento',max_length=40,null=True,blank=True)
    conjuge_cad = models.CharField('Conjuge',max_length=60,null=True,blank=True)
    empresa_cad = models.CharField('Empresa',max_length=40,null=True,blank=True)
    profissao_cad = models.CharField('Profissão',max_length=40,null=True,blank=True)
    procedencia_cad = models.CharField('Procedência',max_length=40,null=True,blank=True)
    cidade_1_cad = models.CharField('Cidade 1',max_length=30,null=True,blank=True)
    cidade_2_cad = models.CharField('Cidade 2',max_length=30,null=True,blank=True)
    mala_direrta_cad = models.CharField('Mala direrta',max_length=1,null=True,blank=True)
    conjugue_cad = models.CharField('Conjugue',max_length=60,null=True,blank=True)
    document_resp_cad = models.CharField('Document responsável',max_length=40,null=True,blank=True)
    num_apto_cad = models.IntegerField('Número apartamento',null=True,blank=True)
    num_apto_and_cad = models.IntegerField('Número apartamento and',null=True,blank=True)
    qtd_hosp_apto_cad = models.IntegerField('Quantidade hóspedes apartamento',null=True,blank=True)
    email_cad = models.EmailField('E-mail',unique=True,null=True,blank=True)
    transmitido_cad = models.CharField('Transmitido',max_length=1,null=True,blank=True)
    tipo_empresa_cad = models.CharField('Tipo de empresa',max_length=1,null=True,blank=True)
    inscr_municipal_cad = models.CharField('Inscrição municipal',max_length=15,null=True,blank=True)
    imp_bruto_cad = models.CharField('Imposto bruto',max_length=1,null=True,blank=True)
    cond_pag_cad = models.IntegerField('Condição de pagamento',null=True,blank=True)
    cod_cairro1_cad = models.IntegerField('Código bairro',null=True,blank=True)
    cod_bairro2_cad = models.IntegerField('Código bairro 2',null=True,blank=True)
   # assinatura_cad = StdImageField('Assinatura',upload_to=get_file_path,variations={'thumb':(225,225)},null=True,blank=True)
    classif_fiscal_cad = models.CharField('Classificação fiscal',max_length=1,null=True,blank=True)
    sal_mansal_atu_cad = models.DecimalField('Salário mensal atual',max_digits=7,decimal_places=2,null=True,blank=True)
    lim_cred_mensal_cad = models.DecimalField('Limite de crédito mensal',max_digits=7,decimal_places=2,null=True,blank=True)
    num_chamada_cad = models.IntegerField('Número chamada',null=True,blank=True)
    nacionalidade_pai_cad = models.CharField('Nacionalidade pai',max_length=15,null=True,blank=True)
    nacionalidade_mae_cad = models.CharField('Nacionalidade mãe',max_length=15,null=True,blank=True)
    indice3_cad  = models.DecimalField('Índice 3',max_digits=7,decimal_places=2,null=True,blank=True)
    malaend_cad = models.CharField('Malaend',max_length=1,null=True,blank=True)
    tipocusto_cad = models.CharField('Tipo custo',max_length=1,null=True,blank=True)
    cod_cidade1_cad = models.IntegerField('Código cidade',null=True,blank=True)
    cod_cidade2_cad = models.IntegerField('Código cidade 2',null=True,blank=True)
    isento_ver_cons_cad = models.CharField('Isento ver cons',max_length=1,null=True,blank=True)
    usu_ult_alt_ise_cad = models.IntegerField('Usuário última alteração',null=True,blank=True)
    data_ult_alt_ise_cad = models.DateTimeField('Data ultima alteracao',null=True,blank=True,default=timezone.now)
    ref_finan_cad = models.CharField('Ref finan',max_length=1,null=True,blank=True)
    procedencia_bolsa_cad = models.IntegerField('Procedência bolsa',null=True,blank=True)
    reg_junta_comerc_cad = models.CharField('Registro Junta Comercial',max_length=15,null=True,blank=True)
    celular_cad = models.CharField('Celular',max_length=15,null=True,blank=True)
    caixa_postal_cad = models.CharField('Caixa postal',max_length=10,null=True,blank=True)
    desper_hora_cad = models.DateTimeField('Desper hora',null=True,blank=True,default=timezone.now)
    desper_data_cad = models.DateTimeField('Desper data',null=True,blank=True,default=timezone.now)
    tipo_vei_cad = models.CharField('Tipo veículo',max_length=15,null=True,blank=True)
    placa_vei_cad = models.CharField('Placa veículo',max_length=10,null=True,blank=True)
    estado_vei_cad = models.CharField('Estado veículo',max_length=2,null=True,blank=True)
    cidade_vei_cad = models.CharField('Cidade veículo',max_length=30,null=True,blank=True)
    cor_vei_cad = models.CharField('Cor veículo',max_length=20,null=True,blank=True)
    suframa_cad = models.CharField('Suframa',max_length=15,null=True,blank=True)
    obs_atendente = models.TextField('Observações atendente',blank=True,null=True)
    blo_des_ven = models.CharField('Bloquear desconto venda',max_length=1,null=True,blank=True)
   # foto_doc_cad = StdImageField('Documento',upload_to=get_file_path,variations={'thumb':(225,225)},null=True,blank=True)
   # foto_doc2_cad = StdImageField('Documento 2',upload_to=get_file_path,variations={'thumb':(225,225)},null=True,blank=True)
    site_cad = models.CharField('Site',max_length=40,null=True,blank=True)

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'   
   

    def __str__(self):
        return str(self.nome_cad)
    



    def get_pk(self:int):
        return self.codigo_cad     
    def get_aniversario(self):
        return f'{self.aniversario_cad.strftime("%d/%m/%Y") if self.aniversario_cad != None else "30/12/1899"}'

    # clica na pessoa e retorna os detalhes dela
    def get_customer_url(self):
        return f'/customer/{self.codigo_cad}'

    # clica em vendas e retorna as vendas da pessoa
    def get_sale_customer_url(self):
        return f'/venda/?customer_sale={self.codigo_cad}'

    # vendas por pessoa
#    def get_sales_count(self):
#        return self.customer_sale.count()
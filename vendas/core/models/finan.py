
import uuid
import re
from django.db import models
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, resolve_url, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.utils.formats import number_format
from django.utils import timezone
from vendas.users.models import User
from vendas.users.models import User
from datetime import date 

class Mov_caixa(models.Model):
	id_mov_Caixa = models.AutoField("Id do caixa",primary_key=True,editable=False)
	mov = models.IntegerField("movimento do caixa ",null =True ,blank=True)
	data_emiss =models.DateTimeField("data de emissao",null = True, editable=False, default=timezone.now,blank=True)
	usu_alt = models.ForeignKey("users.User", null=True ,db_column='cod_usu',related_name='user_USU_mov',verbose_name='usuario do movimento',on_delete=models.CASCADE)
	data_mov = models.DateTimeField("data do movimento do caixa",null=False,blank=False,editable=True)
	valor_baixa = models.DecimalField("valor da baixa " ,null =True , max_digits=9,decimal_places=2,blank=True)
	Troco_inicial = models.DecimalField("Troco inicial", null=True,max_digits=9,decimal_places=2,blank=True)
	saldo_ant = models.DecimalField("saldo anterior", null=True,max_digits=9,decimal_places=2,blank=True)
	cod_seto_mov_c = models.ForeignKey('core.Setor',db_column='cod_seto_mov_c',null=True,related_name='setor_SET_moov',verbose_name='setor do relatorio do caixa',on_delete=models.CASCADE)	
	class Meta:
		ordering = ['id_mov_Caixa']
		verbose_name = 'mov_caixa'
		verbose_name_plural = 'mov_caixas'
	def get_detalhe(self):
		return f'/finan/{self.id_mov_Caixa}'
	def get_Imprime(self):
		return f'finan/cont/{self.id_mov_Caixa}'
class Titulos (models.Model):
	numero_tit = models.AutoField("id titulos",primary_key=True,editable = False)
	data_emissao_tit = models.DateTimeField("data de emissao", blank =True , null = True,default=timezone.now)
	data_venc_tit = models.DateTimeField("data de vencimento", blank =True , null = True,default=timezone.now)
	tipo_tit  = models.CharField("tipo de Titulos ",blank = True , null= True , max_length=1 )
	conta_Ban_tit  = models.IntegerField("",blank=True, null =True )
	caracter_tit =  models.CharField("tipo de caractere ",blank = True , null= True , max_length=1 )
	tipo_mov_tit = models.CharField("tipo de movimento ",blank = True , null= True , max_length=2 )
	numero_mov_tit = models.CharField("numero do movimento", max_length=20,blank =True , null= True )
	nf_tit = models.CharField("nf",max_length=30 ,null=True , blank=True )
	cod_cad_tit = models.IntegerField("codico de cadastro",null=True,blank = True )
	Data_baixa_tit = models.DateTimeField("data da baixa ", null =True ,blank=True)
	tipo_baixa_tit = models.DecimalField("valor da baixa", null = True , blank=True , decimal_places=2 , max_digits=8)
	forma_baixa_tit = models.CharField("forma da baixa",max_length=1, null = True , blank =True )
	num_doc_baixa_tit = models.CharField("forma da baixa",max_length=20, null = True , blank =True )
	obs_tit  = models.CharField("observações ", null =True,max_length= 200, blank = True )
	oper_inclu =models.IntegerField("codigo de inclusao", null =True )
	#oper_D_inclu_tit = models.
	#boleto_tit = models.
	#baixado_tit = models.
	#ger_aut_tit = models.
	#valor_serv_tit = models.
	#oper_venda_tit =models.
	#Oper_d_venda_tit =models.
	#centro_custo_tit = models.
	#Data_cob_tit = models.
	#duplicata_tit = models.
	#periodo_venc_tit = models.
	#tradutor_tit = models.
	#num_boleto_tit = models.
	#cod_cad_interlig_tit = models.
	#irrf_normal = models.
	#irrf_cooperativa = models.
	pis = models.DecimalField("pis ", null = True , blank=True , decimal_places=2 , max_digits=8)
	cofins  = models.DecimalField("cofins ", null = True , blank=True , decimal_places=2 , max_digits=8)
	csll = models.DecimalField("csll ", null = True , blank=True , decimal_places=2 , max_digits=8)
	Issqn =  models.DecimalField("issqn", null = True , blank=True , decimal_places=2 , max_digits=8)
	inss = models.DecimalField("inss ", null = True , blank=True , decimal_places=2 , max_digits=8)
	setor_baixa_tit =models.ForeignKey('core.Setor',db_column='setor_baixa_tit',related_name='setor_titulos',verbose_name='setor_baixa_tit',on_delete=models.CASCADE,null=True)
	class Meta:
		ordering = ['numero_tit']
		verbose_name = 'Titulos'
		verbose_name_plural = 'titulos'
class Saldos (models.Model):
	id_saldos =  models.AutoField("id do saldo ", primary_key = True , blank =True )
	data_sal =  models.DateTimeField("data do saldo ",null = True , blank =True )
	Setor_sal = models.ForeignKey('core.Setor',db_column='Setor_sal',related_name='setor_saldos',verbose_name='Setor_sal',on_delete=models.CASCADE,null=True)
	caracter_salvar = models.CharField("caracter para salvar", max_length= 1 , blank=True, null = True )
	Banco_sal = models.IntegerField("id do banco", null =True , blank = True )
	saldo_sal = models.DecimalField("valor do saldo ", null =True , decimal_places= 2 , max_digits = 8 )
	num_folha_sal = models.IntegerField("numero da folha de OS ", null =True , blank = True )
	Troco_sal =models.DecimalField("valor do troco inicial ", null =True , decimal_places= 2 , max_digits = 8 )
	Supri_cheque_sal = models.DecimalField("valor de cheque ", null = True , blank=True , max_digits=8,decimal_places=2)
	Supri_din_sal =models.DecimalField("valor em dinheiro ", null = True , blank=True , max_digits=8,decimal_places=2)
	Sangria_sal = models.DecimalField("Sangria", null = True , blank=True , max_digits=8,decimal_places=2)
	transf_ent_sal = models.DecimalField("Transferencia entrada ", null = True , blank=True , max_digits=8,decimal_places=2)
	Transf_Said_sal = models.DecimalField("transferencia saida ", null = True , blank=True , max_digits=8,decimal_places=2)
	class Meta:
		ordering = ['data_sal']
		verbose_name = 'Saldo'
		verbose_name_plural = 'Saldos'
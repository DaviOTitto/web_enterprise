from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
#from vendas.core.models import Setor
def upload_image_bock(instance,filename):
	return f'usuarios/{instance.username}/{filename}'
def upload_image_reconhece(instance,filename):
	return f'usuarios/{instance.first_name}/{filename}'



class User(AbstractUser):
	nome_usu = models.CharField(max_length=35,null=True,blank=True)
	funcao_usu = models.CharField(max_length=35,null=True,blank=True)
	cadastro_usu = models.IntegerField(null=True,blank=True)
	position_usu = models.CharField(max_length=35,null=True,blank=True)
	sexo_usu = models.CharField("Sexo",max_length=1,null=True,blank=True)
	acesso_usu = models.TextField("Acesso",null=True,blank=True)
	end_usu = models.CharField("endereco",null=True,blank=True,max_length=254)
	venda_usu = models.CharField("venda",max_length=1,null=True,blank=True)   
	cliente_usu = models.CharField("Cliente",max_length=1,null=True,blank=True)
	fornec_usu = models.CharField("fornecedor",max_length=1,null=True,blank=True)
	item_vend_edit = models.CharField("edit_item_ven",max_length=1,null=True,blank=True)   
	alteraregistro_usu = models.CharField("alterar registros",max_length=1,null=True,blank=True)
	setor_usu = models.ForeignKey('core.Setor',db_column='setor_usu',related_name='setor_user',verbose_name='setor_user',on_delete=models.CASCADE,null=True)
	foto_usu = models.ImageField('Foto',upload_to=upload_image_bock,null=True,blank=True)
	reconhece_1 = models.ImageField('reconhecimento 1',upload_to=upload_image_reconhece,null=True,blank=True)
	reconhece_2 = models.ImageField('reconhecimento 2',upload_to=upload_image_reconhece,null=True,blank=True)
	foto_emp = models.ImageField('Foto da empresa',upload_to=upload_image_bock,null=True,blank=True)
	class Meta:
		ordering = ['id']
		verbose_name = 'usuario'
		verbose_name_plural = 'usuarios'

	def name(self):
		self.nome_usu = first_name;
		return f"{self.first_name} {self.last_name}"

	def get_absolute_url(self):
		return reverse("User_detail",kwargs={"pk":self.pk})

	def get_sale_usuario_url(self):
		return f'/venda/?usuario_sale={self.pk}' 
	def get_detalhe(self):
		return f'/account/{self.pk}/'
	def get_detalhe(self):
		return f'/account/detalhe/{self.pk}/'	

# Create your models here.

# Create your models here.

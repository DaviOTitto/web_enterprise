from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .forms import UserChangeForm,  UserCreationForm
from django.contrib import admin,messages
from .models import *
from import_export.admin import ExportActionMixin,ImportExportModelAdmin
from django.urls import path
from django.shortcuts import redirect

    
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm
	Model= User
	ordering = ['id']
	fieldsets = auth_admin.UserAdmin.fieldsets  + (
		("campos novos", {"fields": ("funcao_usu","cadastro_usu",
			"position_usu","sexo_usu","acesso_usu","end_usu","venda_usu","cliente_usu",
			"fornec_usu","alteraregistro_usu","setor_usu","foto_usu","foto_emp","reconhece_1","reconhece_2")}),
	)
	list_display =( 'id','username','funcao_usu')
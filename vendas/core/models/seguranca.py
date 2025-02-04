import uuid
import re
from django.db import models
from django.urls import reverse, reverse_lazy
#from stdimage.models import StdImageField
from django.utils import timezone
from vendas.users.models import User
import datetime
#from .models import *
#from django.contrib import admin, messages
#from import_export.admin import ExportActionMixin,ImportExportModelAdmin
#modificado Antonio 23/05/2022
from pathlib import Path, os

class Seguranc(models.Model):
	id_Segur  = models.AutoField("id Seguranc",primary_key=True,editable=False,blank=True)
	firma_seg = models.CharField('seguimento da firma', max_length=40,null=True,blank=True)
	foto = models.ImageField(null =True)
	

	def __str__(self):
		return self.firma_seg

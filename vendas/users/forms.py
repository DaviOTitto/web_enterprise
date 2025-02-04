from django.contrib.auth import forms
from rest_framework import serializers

from .models import User

class  UserChangeForm(forms.UserChangeForm):
	class Meta(forms.UserChangeForm.Meta):
		model=User
class UserCreationForm(forms.UserCreationForm):
	class Meta(forms.UserCreationForm.Meta):
		model=User 


#class Seraliser_img(serializers.ModelSerializer):
#	class Meta:
#		model = User
#		fields = ('foto_usu','foto_emp','reconhece_1','reconhece_2')



#class UserEditForm(forms.UserEditForm):
	#class Meta(forms.EditForm.Meta):
		#model = User

		
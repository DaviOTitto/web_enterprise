#django imports
from django.shortcuts import render
from django.contrib import admin
from django.shortcuts import render, resolve_url, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.http import StreamingHttpResponse
from django.urls import path

#local aplications import
from .forms import UserCreationForm,UserChangeForm # seraliser_img
from .models import User


#python imports
import os 
import datetime
import numpy as np
import cv2
import pickle

@login_required
def dashboard(request):
	return render(request,'account/dashboard.html')

@login_required
def register(request):
	Order_forms = User()
	item_order_formset = inlineformset_factory(User,form=UserCreationForm,
											   extra=0,can_delete=False,
											   min_num=1,validate_min=True)
	if request.method == 'POST':
		forms = UserCreationForm(request.POST,request.FILES,
										 instance=order_forms,prefix='main')
		formset = item_order_formset(request.POST,request.FILES,
										 instance=order_forms,prefix='user')
		if forms.is_valid() and formset.is_valid():
			# Cria um objeto para o novo usuário, mas não o salva ainda
			new_user = forms.save(commit=False)
			# Define a senha escolhida
			new_user.set_password(forms.cleaned_data['password'])
			# Salva o objeto User
			forms.save()
			formset.save()
			messages.success(request,'Usuário registrado com sucesso.')
			return redirect('/account/')
	else:
		forms = UserCreationForm(instance=order_forms,prefix='main')
		formset = item_order_formset(instance=order_forms,prefix='user')
	
	context = {
		'forms':forms,
		'formset':formset,	
	}
	return render(request,'account/register.html',context)
@login_required
def criacao_conta(context):	
	if request.method == 'POST':
		user_form = UserCreationForm(instance=order_forms.user,data=request.POST)
		if user_form.is_valid() :
			user_form.save()
			messages.success(request,'Usuário criado com sucesso .')
		else:
			messages.error(request,'Erro ao registrar usuario.')
			return redirect('/account/edit')
	else:
		user_form = UserCreationForm(instance=order_forms.user)
		#retirada de user profile  nome Davi Oliveira Tito 03/05/2022
		#profile_form = UserChangeForm(instance=request.user)
	
	context = {
		'user_form':user_form,
	}
	return render(request,'account/register.html',context)



#def register_done(request):
#	return render(request,'account/register_done.html')

@login_required
def list(request):
	object_list = User.objects.all().order_by('pk')
	user = User.objects.all().order_by('pk')[0:5]
	admin = request.user
	search = request.GET.get('search_box')
	if admin.is_superuser is True: 
		if search:
			object_list = object_list.filter(first_name__icontains=search)
			paginator = Paginator(object_list, 20)
			page = request.GET.get('page', 1)
		#try:
		# 	object_list = paginator.page(page)
		#except PageNotAnInteger:
		#	object_list = paginator.page(1)
		#except EmptyPage:
		#	object_list = paginator.page(paginator.num_pages)
		context = {'object_list':object_list}
		return render(request,'account/list_user.html',context)
	else:
		return render(request,'account/error.html')
@login_required
def error(request):
	object_list = User.objects.all().order_by('pk')
	context = {'object_list':object_list}
	return render(request,'account/error.html',context)

@login_required
def detalhe_usuario(request, pk):
    usuario = get_object_or_404(User,pk=pk)

    context = {
        'usuario':usuario,
    }
    return render(request,'account/user_detail.html',context)
@login_required
def detalhe_usuario2(request, pk):
    usuario = get_object_or_404(User,pk=pk)

    context = {
        'usuario':usuario,
    }
    return render(request,'account/detalhe_usuario.html',context)

@login_required
def edit(request):
	if request.method == 'POST':
		
		user_form = UserChangeForm(instance=request.user,data=request.POST)
		#img_form =  Seraliser_img(instance=request.user,data=request.POST)
		 #remoção de user_profile 03/05/2022
		#profile_form = ProfileEditForm(instance=request.user,data=request.POST,files=request.FILES)
		if user_form.is_valid() :
			user_form.save()
			#if img_form.is_valid():
			#	img_form.save()
			messages.success(request,'Usuário alterado com sucesso.')
			return redirect('/account/')
		else:
			messages.error(request,'Erro ao alterar usuário.')
			return redirect('/account/edit')
	else:
		user_form = UserChangeForm(instance=request.user)
	#	img_form =  Seraliser_img(instance=request.user)
		#retirada de user profile  nome Davi Oliveira Tito 03/05/2022
		#profile_form = UserChangeForm(instance=request.user)
	
	context = {
		'user_form':user_form,
	#	'img_form':img_form,
	}
	return render(request,'account/edit.html',context)

@login_required
def camera(request):
	face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt2.xml')
	recognizer = cv2.face.LBPHFaceRecognizer_create()
	recognizer.read("./recognizers/face-trainner.yml")
	labels = {"person_name": 1} 
	with open("pickles/face-labels.pickle", 'rb') as f:
		og_labels = pickle.load(f)
		labels = {v:k for k,v in og_labels.items()}
	cap = cv2.VideoCapture(0)                
	while(True):
    	# Captura de rosto frame por frame
		ret, frame = cap.read()
		gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
		for (x, y, w, h) in faces:
			roi_gray = gray[y:y+h, x:x+w] 
			roi_color = frame[y:y+h, x:x+w]
			id_, conf = recognizer.predict(roi_gray)
			if conf>=20 and conf <= 85:
				font = cv2.FONT_HERSHEY_SIMPLEX   
				name = labels[id_]
				color = (255, 255, 255)
				stroke = 2
				cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
			img_item = "Cliente.png"
			cv2.imwrite(img_item, roi_color)
			color = (255, 0, 0) 
			stroke = 2
			end_cord_x = x + w
			end_cord_y = y + h
			cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
    	# Display the resulting frame
		cv2.imshow('frame',frame)
		if cv2.waitKey(20) & 0xFF == ord('q'):
			break
	# quando terminar tirar a foto
	cap.release()
	cv2.destroyAllWindows()
	return (edit(request))

def login_camera(request):
	face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt2.xml')
	recognizer = cv2.face.LBPHFaceRecognizer_create()
	recognizer.read("./recognizers/face-trainner.yml")
	labels = {"person_name": 1} 
	with open("pickles/face-labels.pickle", 'rb') as f:
		og_labels = pickle.load(f)
		labels = {v:k for k,v in og_labels.items()}
	cap = cv2.VideoCapture(0)                
	while(True):
    	# Captura de rosto frame por frame
		ret, frame = cap.read()
		gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
		for (x, y, w, h) in faces:
			roi_gray = gray[y:y+h, x:x+w] 
			roi_color = frame[y:y+h, x:x+w]
			id_, conf = recognizer.predict(roi_gray)
			if conf>=20 and conf <= 85:
				font = cv2.FONT_HERSHEY_SIMPLEX   
				name = labels[id_]
				color = (255, 255, 255)
				stroke = 2
				cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
				if name != None : 
					try:
						user = User.objects.filter(username = name)
					except User.DoesNotExist:
						user = None
						name ="username inexistente"
			img_item = "Cliente.png"
			cv2.imwrite(img_item, roi_color)
			color = (255, 0, 0) 
			stroke = 2
			end_cord_x = x + w
			end_cord_y = y + h
			cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
    	# Display the resulting frame
		cv2.imshow('frame',frame)
		if cv2.waitKey(20) & 0xFF == ord('q'):
			break
	return (edit(request))

		
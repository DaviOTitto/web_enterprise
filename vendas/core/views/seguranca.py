from django.shortcuts import render, resolve_url
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator
from rest_framework import viewsets
from ..forms import ImagemSerializer
from vendas.users.models import User
 
from ..models import Cadastro,Seguranc

from vendas.users.forms import UserChangeForm,  UserCreationForm

from vendas.users.admin import UserAdmin
from ..mixins import CounterMixin, FirstnameSearchMixin

@login_required
def User_add(request):
    if request.method == 'POST':  
        form =  UserForm(request.POST)
        if form.is_valid():
            form = form.save()
            return HttpResponseRedirect(resolve_url('core:User_detail', form.pk))
    else:
        form =  UserChangeForm()
    context = {
        'form':form,
    }
    return render(request,'core/person/create_user_form.html',context)

@login_required
def listar_usuarios(request):
    object_list = User.objects.all().order_by('id')
    # pesquisa na lista de usuarios   pelo nome do usuario        
    #def get_queryset(self):
    search = request.GET.get('search_box')
        
        #if search is not None:
    object_list = object_list.filter(username=search)

    paginator = Paginator(object_list, 20)
    page = request.GET.get('page', 1)
    try:
        usuarios = paginator.page(page)
    except PageNotAnInteger:
        usuarios = paginator.page(1)
    except EmptyPage:
        usuarios = paginator.page(paginator.num_pages)

    context = {'usuarios':usuarios}
    return render(request,'core/Seguranca/usuario_list.html',context)


class UserDetail(DetailView):
    template_name = 'core/Seguranca/user_detail.html'
    model = User

class ImagemViewSet(viewsets.ModelViewSet):
    queryset = Seguranc.objects.all()
    serializer_class = ImagemSerializer


class UserUpdate(UpdateView):
    template_name = 'core/Seguranca/User_edit.html'
    model = User
    success_url = reverse_lazy('User_detail')


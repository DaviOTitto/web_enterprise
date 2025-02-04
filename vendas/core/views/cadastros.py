from django.shortcuts import render, resolve_url
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator
from pathlib import Path, os

from ..models import  Cadastro
from ..forms import CadastrosForm
from ..mixins import CounterMixin, FirstnameSearchMixin

@login_required
def  Cadastros_add(request):
    if request.method == 'POST':  
        form = CadastrosForm(request.POST)
        if form.is_valid():
            form = form.save()
            return HttpResponseRedirect(resolve_url('core:cadastros_detail', form.pk))
    else:
        form = CadastrosForm()
    context = {
        'form':form,
    }
    return render(request,'core/person/create_customer_form.html',context)


@login_required
def  Cadastros_list(request):
    object_list = Cadastro.objects.all().order_by('codigo_cad')

    # pesquisa na lista de clientes pelo nome do cliente        
    search = request.GET.get('search_box')
    if search:
        object_list = object_list.filter(nome_cad__icontains=search)

    paginator = Paginator(object_list, 20)
    page = request.GET.get('page', 1)
    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        clientes = paginator.page(1)
    except EmptyPage:
        clientes = paginator.page(paginator.num_pages)

    context = {'clientes':clientes}
    return render(request,'core/person/lista_cadastro.html',context)


class  CadastroDetail(DetailView):
    template_name = 'core/person/cadastro_detail.html'
    model = Cadastro


class  CadastrosUpdate(UpdateView):
    template_name = 'core/person/cadastro_edit.html'
    model = Cadastro
    success_url = reverse_lazy('Cadastros_detail')


from django.shortcuts import render, resolve_url
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator
from pathlib import Path, os

from ..models import Customer
from ..forms import CustomerForm
from ..mixins import CounterMixin, FirstnameSearchMixin

@login_required
def Customer_add(request):
    if request.method == 'POST':  
        form = CustomerForm(request.POST)
        if form.is_valid():
            form = form.save()
            return HttpResponseRedirect(resolve_url('core:customer_detail', form.pk))
    else:
        form = CustomerForm()
    context = {
        'form':form,
    }
    return render(request,'core/person/create_customer_form.html',context)


@login_required
def Customer_list(request):
    object_list = Customer.objects.all().order_by('codigo_cad')

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
    return render(request,'core/person/lista_clientes.html',context)


class CustomerDetail(DetailView):
    template_name = 'core/person/customer_detail.html'
    model = Customer


class CustomerUpdate(UpdateView):
    template_name = 'core/person/customer_edit.html'
    model = Customer
    success_url = reverse_lazy('customer_detail')


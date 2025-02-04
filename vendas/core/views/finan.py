from   vendas.users.models import User
from django.shortcuts import render, resolve_url, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import TemplateView, ListView, DetailView
from django.forms.models import inlineformset_factory
from dateutil.parser import parse
from datetime import timedelta
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import datetime

from ..models import Venda
from ..models import Mov_caixa,Setor
from ..forms import Mov_caixaForm
from ..mixins import CounterMixin
from   vendas.users.models import User
@login_required
def Imprime_mov_caixa(request):
    print("mensagem de teste 1 ")
    order_forms = Mov_caixa() 
    print("mensagem de teste 2 ")
    try:
      print("mensagem de teste 3 ")
      mov_caixa = (Mov_caixa.objects.latest('pk'))
    except Venda.DoesNotExist:
      print("mensagem de teste 4 ")
      mov_caixa = None

    

    setor = Setor.objects.all().order_by('pk')[0:5]
    print("mensagem de teste 5 ")
    #vendas = Venda.objects.all().order_by('pk')
    #item_order_formset = inlineformset_factory(Mov_caixa,form=Mov_caixaForm,
    #                extra=0,can_delete=False,min_num=1,validate_min=True)
    print("mensagem de teste 6 ")
    if mov_caixa == None:
         move_Caixa = 1
    else :
         move_Caixa = (Mov_caixa.objects.latest('pk').id_mov_Caixa+1)
    print("mensagem de teste7 ")
    
    order_forms = Mov_caixa()
    data = datetime.today().strftime("%d/%m/%Y")
    user = User.objects.all().order_by('pk')[0:5]
    print(user)
    print(data)
    # mais uma tentativa falha de usar cod_usu Davi Oliveira Tito 03/05/2022
    if request.method == 'POST':
        print("o erro não esta aqui")
        forms = Mov_caixaForm(request.POST, request.FILES, 
            instance=order_forms, prefix='main')
        user = User.objects.all().order_by('pk')
        usuario_mov = request.user 
        setor = Setor.objects.all().order_by('pk')
        #mov_caixa = Mov_caixa.objects.all().order_by('pk')
        #formset = item_order_formset(request.POST, request.FILES, 
        #    nstance=order_forms, prefix='Mov_caixa')
        print("e nem aqui ")
        if forms.is_valid() :
            print("forms ")
            forms = forms.save(commit=False)
            print(forms.data_mov)
            #forms.cod_seto_mov_c = Setor(pk=request.POST[""])
            #forms.desconto_ven = float(request.POST.get("main-Troco",False))
            # remoção de user_profile e user_id Davi Oliveira Tito 04/04/2022
            # comentario colocado e 1 fixado Davi Oliveira Tito 03/05/202
            #alterando 1 fixado, paracolocar o ID           
            # remoção de user_profile Davi Oliveira Tito 04/04/2022
            # tirando user e fixando 1 03/05/2022                     
            #forms.Troco_inicial= float(request.POST.get("main_troco_inicial",False))
            print("apenas para testes10 ")
            #forms.desconto_ven = Venda(desconto_ven=request.POST[desconto])
            forms.save()
            #formset.save()
            return HttpResponseRedirect(resolve_url('core:imprime_por_data',forms.pk))
        else:
            messages.warning(request,'Erro interno ao IMPRIMIR  o movimento de caixa ')
    else:
        forms = Mov_caixaForm(instance=order_forms, prefix='main')

    # retorna as vendas do cliente, vindo da página de customers
    search = request.GET.get('search-box-setor')
    if search:
        setor = setor.filter(cod_seto_mov_c_descricao_incontains=search)

    context = {
        'forms': forms,
        #'formset': formset,
        #'setor': setor,
        'data': data,
    }

    print("apenas para testes11")
    return render(request,'core/finan/Imprime_mov_caixa.html',context)




@login_required
def listar_Mov_caixa(request):
    
    object_list = Mov_caixa.objects.all().order_by('data_mov')
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    print(data_inicial)
    print(data_final)
    
    if data_inicial and data_final:    
        data_final = parse(data_final) + timedelta(1)
        object_list = object_list.filter(data_mov__range=[data_inicial, data_final])
    search = request.GET.get('search_box')
    
    paginator = Paginator(object_list, 20)
    page = request.GET.get('page', 1)

    try:
        
         mov_caixa = paginator.page(page)
    
    except PageNotAnInteger:
         mov_caixa = paginator.page(1)
    
    except EmptyPage:
        
         mov_caixa = paginator.page(paginator.num_pages)

    
    context = {'mov_caixa':mov_caixa}
    return render(request,'core/finan/lista_Mov_caixa.html',context)
@login_required
def mov_caixa_Detail(request, pk):
    mov_caixa = get_object_or_404(Mov_caixa,pk=pk)
        
        #itens = []
        #itens = ItemVEN.objects.filter(num_ven_ite=pk)
    context = {
    'Mov_caixa':Mov_caixa,
                #'itens':itens,
            }
    return render(request,'core/finan/detalhe_mov_caixa.html',context)

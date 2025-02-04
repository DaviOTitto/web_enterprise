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

from ..models import Venda, ItemVEN, Cadastro, Produto, CondPag,Setor,SetorPRO
from ..forms import VendaForm, ItemVenForm
from ..mixins import CounterMixin
from   vendas.users.models import User

home = TemplateView.as_view(template_name='index.html')
inicio = TemplateView.as_view(template_name='inicio.html')



@login_required
def nova_venda(request):
    order_forms = Venda() 
    
    try:
      venda = (Venda.objects.latest('pk'))
    except Venda.DoesNotExist:
      venda = None

    clientes = Cadastro.objects.all().order_by('pk')[0:5]
    condicoes = CondPag.objects.all().order_by('pk')
    produtos = Produto.objects.all().order_by('pk')[0:5]
    #vendas = Venda.objects.all().order_by('pk')
    item_order_formset = inlineformset_factory(Venda, ItemVEN,form=ItemVenForm,
                    extra=0,can_delete=False,min_num=1,validate_min=True)
    
    if venda == None:
         nmrVenda = 1
    else :
         nmrVenda = (Venda.objects.latest('pk').numero_ven+1)
        # nmrVenda.numero_ven = str(nmrVenda.numero_ven)
    data = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
    # remoção de user_profile  Davi Tito 04/04/2022
    # não funcionou fixar um aqui  Davi Tito 03/05/2022
    user = User.objects.all().order_by('pk')[0:5]
    vendedor = request.user
    setor = Setor.objects.filter(pk=request.user.setor_usu.key_setor)
    
    # mais uma tentativa falha de usar cod_usu Davi Oliveira Tito 03/05/2022
    #cod_usu = 1;
    # teste para vendedor.cod_usu=1 03/05/2022
    # teste deu errado 03/05/2022
    #vendedor.cod_usu = 1;
    
    if request.method == 'POST':
        forms = VendaForm(request.POST, request.FILES, instance=order_forms, prefix='main')
        user = User.objects.all().order_by('pk')
        venda = Venda.objects.all().order_by('pk')
        formset = item_order_formset(request.POST, request.FILES, instance=order_forms, prefix='product')
        produtos = Produto.objects.all().order_by('pk')
     



        if forms.is_valid() and formset.is_valid():
            forms = forms.save(commit=False)
            #forms.numero_ven= nmrVenda.numero_ven
            forms.data_ven = datetime.today()
            forms.cliente_ven = Cadastro(pk=request.POST["main-cliente_ven_aux_cod"])
            # remoção de user_profile e user_id Davi Oliveira Tito 04/04/2022
            # comentario colocado e 1 fixado Davi Oliveira Tito 03/05/202
            #alterando 1 fixado, paracolocar o ID
            forms.usuario_ven = User(pk=request.user.id)
             # remoção de user_profile Davi Oliveira Tito 04/04/2022
             # tirando user e fixando 1 03/05/2022
            forms.setor_ven = request.user.setor_usu.key_setor
            forms.formapag_ven = CondPag(pk=request.POST["main-formapag_ven_aux_cod"])
            i = 0
                     
            
            
            #aux = desconto.value_from_object(desconto)
            forms.desconto_ven = float(request.POST.get("main-desconto_ven",False))
            print("apenas para testes")
            print(forms.desconto_ven)
            #forms.desconto_ven = Venda(desconto_ven=request.POST[desconto])

            for inline_form in formset:
                if inline_form.cleaned_data:
                    inline_form = inline_form.save(commit=False)
                    produto = Produto.objects.filter(pk=request.POST[f'product-{i}-produto_ite_aux_cod'])
                    if produto != None : 
                        inline_form.produto_ite = get_object_or_404(Produto,pk=request.POST[f'product-{i}-produto_ite_aux_cod'].split(' ')[0])     
                        value = float(request.POST.get(f'product-{i}-produto_ite_aux_valor',False))
                        produto = Produto.objects.filter(pk=request.POST[f'product-{i}-produto_ite_aux_cod'])
                        print(produto)
                        if value > 1 :
                        
                            inline_form.unitario_ite = float(request.POST.get(f'product-{i}-produto_ite_aux_valor',False))        
                            inline_form.quantidade_ite = float(request.POST.get(f'product-{i}-produto_ite_aux_quant',False))
                        
                        else :                                                                                                        
                            inline_form.quantidade_ite = float(request.POST.get(f'product-{i}-produto_ite_aux_quant',False))
                            #produto = Produto.objects.filter(pk=request.POST[f'product-{i}-produto_ite_aux_cod']).values_list(produto.get_valor).get()
                        # puxando o setor ao qual o usuario está logado 19/08/2022 Davi Oliveira Tito
                            setor_aux = Setor.objects.filter(pk=request.user.setor_usu.key_setor).values_list('key_setor').get()
                            print(setor_aux)
                        #puxando o id do produto 19/08/2022 Davi Oliveira Tito
                            produto = Produto.objects.filter(pk=request.POST[f'product-{i}-produto_ite_aux_cod']).values_list('produto_pro').get()
                        #print(produto)
                        #Aqui o preco é salvo, Davi Oliveira Tito19/08/2022
                            setor_ven_aux = SetorPRO.objects.filter(num_setor=setor_aux[0],cod_pro_set=produto[0]).values_list('preco_venda_set').get()
                            print(setor_ven_aux)
                            preco = setor_ven_aux[0]
                            #aqui seria aonde salva o preco final (idento a possiveis modific)
                            if setor_ven_aux != None:
                                 inline_form.unitario_ite = setor_ven_aux[0]
                                 print(inline_form.unitario_ite)
                            else :
                                messages.info(request, 'erro na venda, impossivel cadastrar valor da venda ')
                    else :
                        menssages.info(request,'codigo nulo ')  
                                #inline_form.produto_ite = get_object_or_404(Produto,foto_pro=request.POST[f'image-pro-{i}-produto_foto_pro'].split(' ')[0])  
                i = i + 1
            forms.save()
            formset.save()
            return HttpResponseRedirect(resolve_url('core:detalhe_venda',forms.pk))
        else:
            messages.warning(request,'Erro interno ao adicionar a venda!')
    else:
        forms = VendaForm(instance=order_forms, prefix='main')
        formset = item_order_formset(instance=order_forms,prefix='product')

    # retorna as vendas do cliente, vindo da página de customers
    search = request.GET.get('search-box-cliente')
    if search:
        clientes = clientes.filter(cliente_ven__nome_cad__icontains=search)
    
    context = {
        'forms': forms,
        'formset': formset,
        'clientes': clientes,
        'condicoes': condicoes,
        'produtos': produtos,
        'setor_ven': setor,
        'nmrVenda': nmrVenda,    
        'data': data,
        'vendedor': vendedor,
    }
    return render(request,'core/venda/nova_venda.html',context)


@login_required
def listar_vendas(request):
    object_list = Venda.objects.all().order_by('-numero_ven')

    # filtro na lista por datas
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    print(data_inicial)
    print(data_final)
    if data_inicial and data_final:
        data_final = parse(data_final) + timedelta(1)
        object_list = object_list.filter(data_ven__range=[data_inicial, data_final])

    # pesquisa na lista de vendas pelo nome do cliente        
    search = request.GET.get('search_box')
    if search:
        object_list = object_list.filter(cliente_ven__nome_cad__icontains=search)

    # retorna as vendas do cliente, vindo da página de customers
    if 'cadastros_sale' in request.GET:
        object_list = object_list.filter(cliente_ven=request.GET['cadastros_sale'])

    # retorna as vendas do usuário, vindo da página de usuários
    if 'usuario_sale' in request.GET:
        object_list = object_list.filter(usuario_ven=request.GET['usuario_sale'])

    # retorna as vendas do setor, vindo da página de setor    
    if 'setor_sale' in request.GET:
        object_list = object_list.filter(setor_ven=request.GET['setor_sale'])

    paginator = Paginator(object_list, 20)
    page = request.GET.get('page', 1)
    try:
        vendas = paginator.page(page)
    except PageNotAnInteger:
        vendas = paginator.page(1)
    except EmptyPage:
        vendas = paginator.page(paginator.num_pages)

    context = {'vendas':vendas}
    return render(request,'core/venda/lista_vendas.html',context)


@login_required
def detalhe_venda(request, pk):
    venda = get_object_or_404(Venda,pk=pk)
    itens = []
    itens = ItemVEN.objects.filter(num_ven_ite=pk)
    context = {
        'venda':venda,
        'itens':itens,
    }
    return render(request,'core/venda/detalhe_venda.html',context)


@login_required
def deleta_venda(request,pk):
    ItemVEN.objects.filter(num_ven_ite=pk).delete()
    get_object_or_404(Venda,pk=pk).delete()
    return redirect('core:listar_vendas')


@login_required
def altera_venda(request,pk):
    order_forms = Venda()
    item_order_formset = inlineformset_factory(Venda,ItemVEN,form=ItemVenForm,extra=0,can_delete=False,min_num=1,validate_min=True)
    venda = get_object_or_404(Venda,pk=pk)                        # recupera venda
    vendas =  Venda.objects.all().order_by('pk')
    if vendas.desconto_ven != None:
        desconto = f'{vendas.desconto_ven:,2}'
    else :
        vendas.desconto_ven = 0        
        desconto = f'{Venda.desconto_ven:,2}'                      # formata desconto
 # para recuperar os dados do cliente da venda
    clientes = Cadastros.objects.all().order_by('pk')              # para o modal clientes    
    user = User.objects.all().order_by('pk')
    cliente = get_object_or_404(Cadastros,codigo_cad=venda.cliente_ven.codigo_cad)
    #cliente = get_object_or_404(Customer,pk=venda.cliente_ven)    #cliente = get_object_or_404(Customer,pk=venda.cliente_ven)
    produtos = Produto.objects.all().order_by('pk')                # para o modal produtos
    itens = ItemVEN.objects.filter(num_ven_ite=pk)                 # recupera itens venda
    itens_venda = []
    i = 1
    for i in range(itens.count()):
        produto = get_object_or_404(Produto,produto_pro=itens[i].produto_ite.produto_pro)
        #produto = Produto.objects.filter(descricao_pro__descricao_pro=descricao_pro).order_by(produto_pro)
        itens_venda.append(produto.produto_pro)
        itens_venda.append(produto.descricao_pro)
    quantidade_ITEVEN = ItemVEN.objects.values_list('cod_itemven').last()[0]

    if request.method == 'GET':
        forms = VendaForm(instance=venda,prefix='main')
        formset = item_order_formset(instance=venda,prefix='product')
    else:
        forms = VendaForm(request.POST,request.FILES,instance=venda,prefix='main')
        formset = item_order_formset(request.POST,request.FILES,instance=venda,prefix='product')
        if forms.is_valid() and formset.is_valid():
            forms = forms.save(commit=False)
            forms.cliente_ven = get_object_or_404(Customer,pk=request.POST["main-cliente_ven_aux_cod"].split(' ')[0])
            # apagado user.profile da linha 163 , Davi Oliveira Tito 02/05/2022
            forms.usuario_atu_ven_id = request.user.id
            forms.data_atu_ven = datetime.today()
            i = 0
            for inline_form in formset:
                inline_form = inline_form.save(commit=False)
                inline_form.produto_ite = get_object_or_404(Produto,pk=request.POST[f'product-{i}-produto_ite_aux_cod'].split(' ')[0])
                i += 1
            ItemVEN.objects.filter(num_ven_ite=pk).delete()
            forms.save()
            formset.save()
            return HttpResponseRedirect(resolve_url('core:detalhe_venda',forms.pk))
        else:
            messages.warning(request,'Erro interno ao alterar a venda!')
    context = {
        'forms':forms,
        'formset':formset,
        #'desconto':desconto,
        'cliente':cliente,
        'clientes':clientes,
        'produtos':produtos,
        'itens_venda':itens_venda,
        'quantidade_ITEVEN':quantidade_ITEVEN,
    }
    return render(request,'core/venda/altera_venda.html',context)
@login_required
def produto_modal(request):
#   object_list  = SetorPRO.objects.filter(
#                        produto_SETPRO=request.user.user_profile.Setor_USU_id)
    produtos = Produto.objects.all().order_by('descricao_pro')
    search = request.GET.get('search_box')
    if search: #q is not None:
        object_list = object_list.filter(descricao_pro__icontains=search)
        #return object_list

    context = {
        'produtos':produtos,
    }
    return render(request,'core/venda/modal/modal_produto.html',context)

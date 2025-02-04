from django.shortcuts import render, resolve_url, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.forms.models import inlineformset_factory
from django.core.paginator import Paginator

from ..models import Produto, GrupoPRO, SetorPRO , TipoPRO , Cadastro ,Setor 
from  vendas.users.models import User
from ..forms import ProdutoForm, SetorProForm ,TipoPROForm ,CadastrosForm
from ..mixins import FirstnameSearchMixin

@login_required
def novo_produto(request):
    order_forms = Produto()
    item_order_formset = inlineformset_factory(Produto, SetorPRO, 
                                               form=SetorProForm,
                                               extra=0, can_delete=False, 
                                               min_num=1, validate_min=True)
    if request.method == 'POST':
        forms = ProdutoForm(request.POST, request.FILES,
                            instance=order_forms, prefix='main')
        formset = item_order_formset(request.POST, request.FILES,
                                     instance=order_forms, 
                                     prefix='produto')
        if forms.is_valid() and formset.is_valid():
            forms.save()
#            formset = formset.save(commit=False,instance=forms)
#            formset.Codigo_SET_SETPRO = 1
#            formset.Codigo_PRO_SETPRO = 4
            formset.save()
            return HttpResponseRedirect(resolve_url('core:produto_detail',
                                                    forms.pk))
    else:
        forms = ProdutoForm(instance=order_forms, prefix='main')
        formset = item_order_formset(instance=order_forms,
                                     prefix='produto')
    context = {
        'forms': forms,
        'formset': formset,
    }
    return render(request,'core/produto/novo_produto.html',context)


@login_required
def altera_produto(request,pk):
    setorpro = get_object_or_404(SetorPRO,pk=pk)
    produto = Produto.objects.filter(Descricao_PRO=setorpro)
    order_forms = Produto()
    item_order_formset = inlineformset_factory(Produto,SetorPRO,
                                               form=SetorProForm,extra=0,
                                               can_delete=False,min_num=1,
                                               validate_min=True)
    if request.method == 'POST':
        forms = ProdutoForm(request.POST,request.FILES,instance=setorpro,
                            prefix='main')
        formset = item_order_formset(request.POST,request.FILES,
                                     instance=produto,
                                     prefix='Codigo_PRO_SETPRO')
        if forms.is_valid() and formset.is_valid():
            forms = forms.save()
            formset.save()
            return HttpResponseRedirect(resolve_url('core:detalhe_produto',
                                                    forms.pk))
        else:
            forms = VendaForm(instance=setorpro,prefix='main')
            formset = item_order_formset(instance=produto,
                                         prefix='Codigo_PRO_SETPRO')
        context = {
            'forms':forms,
            'formset':formset,
            }
        return render(request,'core/produto/altera_produto.html',context)   
    elif(request.method == 'GET'):
        return render(request,'core/produto/altera_produto.html',
                      {'forms':forms,'formset':formset,})


@login_required
def deleta_produto(request,pk):
    SetorPRO.objects.filter(pk=pk).delete()
    Produto.objects.filter(pk=pk).delete()
    return redirect('core:lista_produto')


@login_required
def ProdutoList(request):
#   object_list  = SetorPRO.objects.filter(
#                        produto_SETPRO=request.user.user_profile.Setor_USU_id)
    object_list = Produto.objects.all().order_by('descricao_pro')
    search = request.GET.get('search_box')
    if search: #q is not None:
        object_list = object_list.filter(descricao_pro__icontains=search)
        #return object_list

    context = {
        'object_list':object_list,
    }
    return render(request,'core/produto/lista_produto.html',context)


#def ProdutoList(request):
 #   user = User.objects.all().order_by('pk')
 #   object_list  = SetorPRO.objects.filter(
 #                       num_setor=request.user.setor_usu)
 #   #object_list = Produto.objects.all().order_by('produto_pro')
 #   user = User.objects.all().order_by('pk')
 #   func = request.user 
 #   def get_queryset(self):
 #     #setando valores do produto 
 #       q = self.request.GET.get('search_box')
 #       if q is not None:
 #         object_list = object_list.filter(
 #                               Codigo_PRO_SETPRO__descricao_pro__icontains=q)
 #         valor = SetorPRO.objects.filter(cod_pro_set = object_list.produtro_pro , num_setor = user.setor_usu).values(preco_venda_set)
 #           print(valor)
 #        return object_list

##    context = {
 #       'object_list':object_list,
 ##   }
    return render(request,'core/produto/modal_produto.html',context)
#criando o def TipoPROList, 11/05/2022
@login_required
def TipoPROList(request):
#   object_list  = SetorPRO.objects.filter(
#                        produto_SETPRO=request.user.user_profile.Setor_USU_id)
    object_list = TipoPRO.objects.all().order_by('id_tipopro')
    def get_queryset(self):
        q = self.request.GET.get('search_box')
        if q is not None:
            object_list = object_list.filter(
                                Codigo_PRO_SETPRO__descricao_pro__icontains=q)
        return object_list

    context = {
        'object_list':object_list,
    }
    return render(request,'core/produto/lista_tipopro.html',context)

# adiçao de novo_TIPOPRO , Davi Oliveira Tito 16/05/2022
@login_required
def novo_TipPRO(request):
    order_forms = TipoPRO()
    item_order_formset = inlineformset_factory(TipoPRO,
                                               form=TipoPROForm,
                                                extra=0, can_delete=False, 
                                               min_num=1, validate_min=True)
    if request.method == 'POST':
        forms = TipoproForm(request.POST, request.FILES,
                            instance=order_forms, prefix='main')
        formset = item_order_formset(request.POST, request.FILES,
                                     instance=order_forms, 
                                     prefix='tipo_pro')
        if forms.is_valid() and formset.is_valid():
            forms.save()
#            formset = formset.save(commit=False,instance=forms)
#            formset.Codigo_SET_SETPRO = 1
#            formset.Codigo_PRO_SETPRO = 4
            formset.save()
            return HttpResponseRedirect(resolve_url('core:tipoPRO_detail',
                                                    forms.pk))
    else:
        forms = TipoproForm(instance=order_forms, prefix='main')
        formset = item_order_formset(instance=order_forms,
                                     prefix='tipo produto')
    context = {
        'forms': forms,
        'formset': formset,
    }
    return render(request,'core/produto/novo_Tipopro.html',context)

def SetorProdutoList(request):
    user = User.objects.all().order_by('pk')
    object_list  = SetorPRO.objects.filter(
                        num_setor=request.user.setor_usu)
    object_list = Produto.objects.all().order_by('produto_pro')
    user = User.objects.all().order_by('pk')
    func = request.user
    def get_queryset(self):
      #setando valores do produto 
        q = self.request.GET.get('search_box')
        if q is not None:
            object_list = object_list.filter(
                                Codigo_PRO_SETPRO__descricao_pro__icontains=q)
            valor = SetorPRO.objects.filter(cod_pro_set = object_list.produtro_pro , num_setor = user.setor_usu).values(preco_venda_set)
            print(valor)
        return object_list

    context = {
        'object_list':object_list,
    }
    return render(request,'core/venda/modal/modal_produto2.html',context)



class tipoPRODetail(DetailView):
    template_name = 'core/produto/detalhe_TipPRO.html'
    model = TipoPRO

class ProdutoDetail(DetailView): 
    model = SetorPRO
    template_name = 'core/produto/detalhe_setorproduto.html'
@login_required

def detalhe_produto(request, pk):
    produto = get_object_or_404(Produto,produto_pro=pk)
    user = User.objects.all().order_by('pk')
    setor = Setor.objects.filter(pk=request.user.setor_usu.key_setor)
    setorpro = get_object_or_404(SetorPRO,cod_pro_set=produto.produto_pro)

    context = {
        'produto':produto,
        'setor':setor,
        'setorpro':setorpro,
    }
    return render(request,'core/produto/detalhe_setorproduto.html',context)




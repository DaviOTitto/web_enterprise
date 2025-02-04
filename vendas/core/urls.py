from django.urls import include, path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
#from django.conf.urls.static import media 
from rest_framework import routers
from .views import *

app_name = 'core'

cadastros_patterns = [
    path('',view=Cadastros_list,name='lista_cadastros'),    
    path('<int:pk>/',login_required(CadastroDetail.as_view()),name='cadastros_detail'),
    path('edit/<int:pk>/',login_required(CadastrosUpdate.as_view()),name='cadastros_update'),
    path('add/',view=Cadastros_add,name='cadastros_add')
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# criando um link para o tipopro , Davi Oliveira tito 11/05/2022
# adiconado o endereço da tela NOVOTIPOPRO, Davi Oliveira Tito 16/05/2022
# adcionado TipoPRODetail Davi 20/05/2022
produto_patterns = [
    path('',ProdutoList,name='lista_produto'),
    path('list',SetorProdutoList,name='setorprodutoList'),
    path('tipopro/',TipoPROList,name='lista_tipoPRO'),
    path('novo_tippro/',novo_TipPRO,name ='novo_tipPRO'),
    path('novo/',view=novo_produto,name='novo_produto'),
    #path('<int:pk>/',login_required(tipoPRODetail.as_view()),name='detalhe_TipoPRO'),
    path('<int:pk>/',view=detalhe_produto,name='detalhe_produto'),
    #path('<int:pk>/',login_required(ProdutoDetail.as_view()),name='detalhe_produto'),
    path('alterar/<int:pk>/',view=altera_produto,name='altera_produto'),
    path('delete/<int:pk>/',view=deleta_produto,name='deleta_produto'),
    path('cupom/<int:pk>/',view=cupom,name='cupom'),
]

venda_patterns = [
    path('',view=listar_vendas,name='listar_vendas'),
    path('nova/',view=nova_venda,name='nova_venda'),
    path('modal_pro/',view=produto_modal,name='produto_modal'),
    path('<int:pk>/',view=detalhe_venda,name='detalhe_venda'),
    path('alterar/<int:pk>/',view=altera_venda,name='altera_venda'),
    path('delete/<int:pk>/',view=deleta_venda,name='deleta_venda'),
    path('ci/<int:pk>/',view=controle_interno,name='controle_interno'),
    path('nfce/<int:pk>/',view=cupom_fiscal,name='cupom_fiscal'),
 #   path('cupom/<int:pk>/',view=cupom,name='cupom'),
]

setor_patterns = [
    path('',login_required(SetorList.as_view()),name='setor_list'),
    path('<int:pk>/',login_required(SetorDetail.as_view()),name='setor_detail'),
]
finan_patterns = [
    #path('Imprime_mov_caixa/',view =Imprime_mov_caixa,name='Imprime_mov_caixa'),
    path('',view =listar_Mov_caixa,name='listar_mov_caixa'),
    path('<int:pk>/',view=mov_caixa_Detail,name='mov_caixa_Detail'),
    path('relatorio/',view = Imprime_mov_caixa,name ='Imprime_mov_caixa'),
    path('impressao/',view =mov_caixa_geral,name='Imprime_mov_geral'),
    path('impressaoM/',view =mov_caixaM,name='Imprime_mov_M'),
    path('impressaoFM/<int:pk>/',view = mov_caixaM_filtro,name='imprime_por_data'),
    path('cont/<int:pk>',view = mov_caixa ,name='Imprime_mov'),
]

seguranca_patterns = [
    path('',view=listar_usuarios,name='listar_usuarios'),    
    path('<int:pk>/',login_required(UserDetail.as_view()),name='user_detail'),
   # path('edit/<int:pk>/',login_required(UserUpdate.as_view()),name='user_update'),
   # path('add/',view=User_add,name='user_add')
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = [
    path('',inicio,name='inicio'),
    path('home/', home, name='home'),
    path('cadastro/', include(cadastros_patterns)),
    path('produto/', include(produto_patterns)),
    path('venda/', include(venda_patterns)),
    path('setor/', include(setor_patterns)),
    path('seguranca/', include(seguranca_patterns)),
    path('finan/',include(finan_patterns)),
]



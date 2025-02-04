import io
import locale
from django.shortcuts import get_object_or_404, redirect
from django.http import FileResponse
from django.contrib import messages
from datetime import datetime
from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import cm, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

from   vendas.users.models import User
from ..models import Mov_caixa,Setor
from ..forms import Mov_caixaForm
from ..mixins import CounterMixin 
from  vendas.users.models import User
from ..models import Venda, Cadastro,Setor 
from ..models import ItemVEN, Produto, CondPag


locale.setlocale(locale.LC_ALL, '')
def formataValor(valor):
    return "R$ {}".format(locale.format("%.2f",valor,grouping=True,monetary=True))

def formataPorcent(valor):
    return "{}%".format(locale.format("%.2f",valor,grouping=True,monetary=True))

def mov_caixa_geral(request):
    
    print("teste 1 ")
    alt_ini = 55
    tf = 7 # Tamanho da fonte
    pl = 8 # Pulo de linha
    data = datetime 
    mov_caixa = get_object_or_404(Mov_caixa,pk=pk)
    total_ent = 0
    total_sai = 0
    troco = float(0.00)
    print(mov_caixa.data_mov)
    troco = float(0.00)
    mov_caixa = Mov_caixa.objects.all().order_by('pk')
    #setor= mov_caixa.objects.filter(pk= object_list.cod_seto_mov_c).order_by(pk)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer,pagesize=(7.9*cm,0*cm),bottomup=0,pageCompression=0,verbosity=0,)
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    pdfmetrics.registerFont(TTFont('ArialBd', 'ArialBd.ttf'))
    p.setFont("Arial",tf)
    p.setTitle(f'Relatorio de movimento de caixa')#{datetime.today().strftime("%d/%m/%Y")})
    p.drawImage('./vendas/core/static/img/logo_cabecalho.bmp',62.5,5,width=100,height=50,preserveAspectRatio=True,mask=None)
    print("teste 2 ")
    def cabecalho_mov(self,alt_ini,troco):
        print("teste 3  ")
        titulos = 0
        mome_cad= 0
        movimento =00000
        esp = 0000
        data = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
        p.drawCentredString(224/2, alt_ini+pl, f'MOVIMENTO DE CAIXA:{data}')
       # p.drawCentredString(224/2, alt_ini+pl, f'empresaVenda.razao_ca - Fone: empresaVenda.telefone1_cad')
        #p.drawCentredString(224/2, alt_ini+pl*2, f'CNPJ: empresaVenda.cgc_cpf_cad - EI: empresaVenda.ie_cad')
        #p.drawCentredString(224/2, alt_ini+pl*3, f'empresaVenda.rua1_cad - empresaVenda.bairro1_cad')
        #p.drawCentredString(224/2, alt_ini+pl*5, f'Setor: {setor.key_setor} titulos:{formataValor(titulos)}')
        #p.drawCentredString(224/2, alt_ini+pl*6, f'nome_cadastro:TESTE  movimentos:{formataValor(movimento)}')
        #p.drawCentredString(224/2, alt_ini+pl*7, f'esp{formataValor(esp)} Entradas  Saidas')
        contador= 1 ;
        p.line(0,alt_ini+pl*2,224,alt_ini+pl*2)
        p.setFont('Arial',tf)
        p.drawString(9,alt_ini+pl*3,f'setor:')
        p.drawString(79,alt_ini+pl*3,f'titulos:' )
        p.drawString(150,alt_ini+pl*3,'nome_cad:')
        p.drawString(9,alt_ini+pl*4,'Docum:')
        p.drawString(79,alt_ini+pl*4,'movimento')
        p.drawString(150,alt_ini+pl*4,'esp')
        p.line(0,alt_ini+pl*5,224,alt_ini+pl*5)
        print("teste 4  ")
        cont = 6 
        troco = 0
        for i in range(mov_caixa.count()): 
            teste = i + 4 
            print(cont)
            setor = Setor.objects.get(pk=mov_caixa[i].cod_seto_mov_c.key_setor)
            p.drawString(9,alt_ini+(pl*cont),f'{mov_caixa[i].id_mov_Caixa}')
            print('teste id ')
            p.drawString(79,alt_ini+(pl*cont),f'{setor.key_setor}')
            print('teste setor ')
            p.drawString(150,alt_ini+(pl*cont),"nome")
            cont = cont + 1 
            p.drawString(9,alt_ini+(pl*cont),"docum")  
            p.drawString(79,alt_ini+(pl*cont),f'{movimento}')  
            p.drawString(150,alt_ini+(pl*cont),f'{esp}')
            soma = float(mov_caixa[i].Troco_inicial)
            
            troco = soma + troco     
            cont = cont + 1 
        
        p.line(0,alt_ini+(pl*cont),224,alt_ini+(pl*cont))        
        return alt_ini+(pl*cont)
    def resumo_impressao_caixa(self,alt_ini):
        print("teste20")
        #valor_produtos = 0
        #for i in range(itens.count()):
        #    produto = Produto.objects.get(produto_pro=itens[i].produto_ite_id)
        #    valor_produtos += itens[i].quantidade_ite * itens[i].unitario_ite
        p.drawString(9,alt_ini,'A vista ')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl,'Boleto Bancario')
        p.drawRightString(200,alt_ini+pl,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,'Contra Apres.')
        p.drawRightString(200,alt_ini+pl*2,f'{formataValor(0)}')
        p.drawString(9,alt_ini,'Cheque pré')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl,'Carteira')
        p.drawRightString(200,alt_ini+pl,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,'cheque pre datado')
        p.drawRightString(200,alt_ini+pl*2,f'{formataValor(0)}')
        p.drawString(9,alt_ini,'Convenio')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl,'Cartao')
        p.drawRightString(200,alt_ini+pl,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,'Troco inicial')
        p.drawRightString(215,alt_ini+pl*2,f'{formataValor(troco)}')
        p.drawString(9,alt_ini,'Vendasa vista')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl,'dv+ tk clientes (-)')
        p.drawRightString(200,alt_ini+pl,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,'np+ca+ct')
        p.drawRightString(200,alt_ini+pl*2,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*3,'Saidas(-) (- Dv+Tr)')
        p.drawRightString(200,alt_ini+pl*3,f'{formataValor((0))}%')
        p.drawRightString(200,alt_ini+pl*3,f'{formataValor((0))}%')
        alt_ini += pl*4.5
        p.drawString(9,alt_ini,'suprimento -cheques')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
       # p.drawString(9,alt_ini+pl,f'{condicao.descricao if venda.condicao_ven != None else "Dinheiro"}')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,f'TRansf - Entradas')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,f'Nota Fiscal')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,f'Nota Promissória')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,f'- Vale')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,f'Convênio')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,f'Outros')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.line(0,alt_ini+pl*2.5,224,alt_ini+pl*2.5)
        p.drawRightString(200,alt_ini+pl*4,f'{formataValor(mov_caixa.Troco_inicial)}')
        print("teste21")
        return alt_ini + pl*3.5
    

    def subtotal_mov_caixa (self,alt_ini):
        troco = 0
        for i in range(mov_caixa.count()): 
            soma = float(mov_caixa[i].Troco_inicial)
            troco = soma +troco    
        print("teste20")
        soma_tudo = 0
        print(soma_tudo)
        p.drawString(9,alt_ini,'A - A vista ')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl,'B - Boleto Bancario')
        p.drawRightString(200,alt_ini+pl,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,'C - Contra Apres.')
        p.drawRightString(200,alt_ini+pl*2,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*3,'D - Cheque pré')
        p.drawRightString(200,alt_ini+pl*3,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*4,'E - Carteira')
        p.drawRightString(200,alt_ini+pl*4,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*5,'F - Duplicada')
        p.drawRightString(200,alt_ini+pl*5,f'{formataValor(0)}')
        p.line(0,alt_ini+pl*6,224,alt_ini+pl*6)
        p.drawString(9,alt_ini+pl*7,'G - Nota Fiscal')
        p.drawRightString(200,alt_ini+pl*7,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*8,'H - Nota Promissória')
        p.drawRightString(200,alt_ini+pl*8,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*9,'I  - Vale .')
        p.drawRightString(200,alt_ini+pl*9,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*10,'J - Cartão-pix')
        p.drawRightString(200,alt_ini+pl*10,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*11,'K - convenio')
        p.drawRightString(200,alt_ini+pl*11,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*12,'L - Outros(RP,XX,CX)')
        p.drawRightString(200,alt_ini+pl*12,f'{formataValor(0)}')
        p.line(0,alt_ini+pl*13,224,alt_ini+pl*13)
        p.drawString(9,alt_ini+pl*14,'Cheque pre datado')
        p.drawRightString(200,alt_ini+pl*14,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*15,'Convenio')
        p.drawRightString(200,alt_ini+pl*15,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*16,'Cartao')
        p.drawRightString(200,alt_ini+pl*16,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*17,'Troco inicial')
        p.drawRightString(200,alt_ini+pl*17,f'{formataValor(troco)}')
        p.drawString(9,alt_ini+pl*18,'Vendasa vista')
        p.drawRightString(200,alt_ini+pl*18,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*19,'DV+ TK clientes (-)')
        p.drawRightString(200,alt_ini+pl*19,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*20,'NP+CA+CT')
        p.drawRightString(200,alt_ini+pl*20,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*21,'Saidas(-) (- Dv+Tr)')
        p.drawRightString(200,alt_ini+pl*21,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*22,'suprimentos-cheques')
        p.drawRightString(200,alt_ini+pl*22,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*23,'suprimentos-dinheiro')
        p.drawRightString(200,alt_ini+pl*23,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*24,'Sangria/Retirada')
        p.drawRightString(200,alt_ini+pl*24,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*25,'TRanst-entradas')
        p.drawRightString(200,alt_ini+pl*25,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*26,'Transt-saidas')
        p.drawRightString(200,alt_ini+pl*26,f'{formataValor(0)}')
        #p.drawString(9,alt_ini+pl,f'{condicao.descricao if venda.condicao_ven != None else "Dinheiro"}')
        #p.drawRightString(9,alt_ini*15,f'Sangria/Retirada (-)')
       # p.drawRightString(215,alt_ini+pl*15,f'{formataValor((0))}')
        #p.drawString(9,alt_ini+pl*16,f'TRansf - Entradas')
        #p.drawRightString(215,alt_ini+pl*16,f'{formataValor((0))}')
        #p.drawRightString(9,alt_ini*17,f'tans-saidas')
        #p.drawRightString(215,alt_ini+pl*17,f'{formataValor((0))}')
        #p.drawString(9,alt_ini*18,f'Caixa FInal')
        #Modificado (retirado + venda.acrescimo_ven) Rennan 03/05/2022
        #modificado(retirado venda.desconto) Davi O 03/05/2022
        #p.drawRightString(210,alt_ini+pl*18,f'{formataValor(0)}')#venda.desconto_ven)}')
        p.line(0,alt_ini+pl*28,224,alt_ini+pl*28)
        #p.drawString(7,alt_ini+pl*5.5,'Data do Vencimento')
        #p.drawRightString(210,alt_ini+pl*5.5,'Valor do Pagamento')
        #p.drawString(7,alt_ini+pl*6.5,f'{mov_caixa.get_data_ven()}')
        #Modificado (retirado + venda.acrescimo_ven) Rennan 03/05/2022
        # modificado(retirado venda.desconto) Davi O 03/05/2022
        p.drawString(9,alt_ini+pl*29,'Caixa Final')
        p.drawRightString(210,alt_ini+pl*29,f'{formataValor((soma_tudo) +troco   )}')#venda.desconto_ven#)}')
        p.line(0,alt_ini+pl*30,224,alt_ini+pl*30)
        print("teste23")
        return alt_ini+pl*32  
    def itens_MOVCAIXA(self,alt_ini):
        produto = ''
        cont = 1 
        for i in range(mov_caixa.count()): 
            cont = 1 + cont 
        p.drawCentredString(224/2,alt_ini+pl,'numero de vendas ')
        p.drawCentredString(224/2,alt_ini+pl*2,f'{cont}')
        p.line(0,alt_ini+pl*3,224,alt_ini+pl*3)
        p.drawString(9,alt_ini+pl*5,'saidas ')
        p.drawString(9,alt_ini+pl*4,'entradas')
        p.line(0,alt_ini+pl*5.5,224,alt_ini+pl*5.5)
        p.drawCentredString(224/2,alt_ini+pl*6.5,'titulos baixados ')  
        

        p.line(0,alt_ini+pl*7,224,alt_ini+pl*7)
        return alt_ini + pl* 8
    def porcentagem_caixa(self,alt_ini):
        p.drawString(9,alt_ini+pl,f'produtos a vista')
        p.drawRightString(200,alt_ini+pl,f'{formataValor((0))+"---"+formataPorcent((0))}')
        p.drawString(9,alt_ini+pl*2,f'servicos a vista')
        p.drawRightString(200,alt_ini+pl*2,f'{formataValor((0))+"---"+formataPorcent((0))}')
        p.drawString(9,alt_ini+pl*3,f'produtos a praso')
        p.drawRightString(200,alt_ini+pl*3,f'{formataValor((0))+"---"+formataPorcent((0))}')
        p.drawString(9,alt_ini+pl*4,f'servico a praso')
        p.drawRightString(200,alt_ini+pl*4,f'{formataValor((0))+"---"+formataPorcent((0))}')
        p.line(0,alt_ini+pl*5,224,alt_ini+pl*5)
        return alt_ini + pl* 6
    def caixa_final(self, alt_ini):
        p.drawString(9,alt_ini+pl*2,f'caixa final')
        p.drawRightString(200,alt_ini+pl*3,f'{formataValor((0))}')
        p.drawString(9,alt_ini+pl*2,f'diferencial de caixa ')
        p.drawRightString(200,alt_ini+pl*3,f'{formataValor((0))}')
        print("teste25")    
        return alt_ini + pl*5
    



    def observacoes_caixa (self,alt_ini):
        p.drawString(7,alt_ini,'OBSERVAÇÕES:')
       # count = len(venda.obs_ven) / 40 if venda.obs_ven != None else 0
       # if count > 1:
       #     parada = 0
       #     i = 0
       #     while i < count:
       #         if i > 5:
       #             break
       #         p.drawString(7,alt_ini+(pl*(i+1)),f'{venda.obs_ven[parada:parada+40]}')
       #         i += 1
       #         parada += 40
        #else:            
        #p.drawString(7,alt_ini+pl,f'{venda.obs_ven if venda.obs_ven != None else ""}')
        p.drawString(152,alt_ini+pl*7,'Versão:1.0')
        p.line(0,alt_ini+pl*6.7,150,alt_ini+pl*6.7)
        p.line(0,alt_ini+pl*6.8,150,alt_ini+pl*6.8)
        p.line(193,alt_ini+pl*6.7,224,alt_ini+pl*6.7)
        p.line(193,alt_ini+pl*6.8,224,alt_ini+pl*6.8)
        print("teste26")
        return alt_ini+pl*8
    def total_geral (self,alt_ini):
        p.drawString(9,alt_ini+pl,f'valor total ')
        p.drawRightString(200,alt_ini+pl,f'{formataValor((0))}')
        p.drawString(9,alt_ini+pl*2,'saldo anterior')
        p.drawRightString(200,alt_ini+pl*2,f'{formataValor((0))}')
        print("teste27")
        p.line(0,alt_ini+pl*3,224,alt_ini+pl*3)
        return alt_ini+pl*4
    def rodape_caixa(self,alt_ini):
        #p.drawCentredString(224/2,alt_ini,'Não é Documento Fiscal')
        p.drawCentredString(224/2,alt_ini+pl,'MOVIMENTO DE CAIXA ')
        p.drawString(78,alt_ini+pl*2,f'{datetime.today().strftime("%d/%m/%Y")} {datetime.today().strftime("%H:%M:%S")}')
        return alt_ini+pl*7

    alt_ini = cabecalho_mov(p,alt_ini,troco)
    alt_ini = itens_MOVCAIXA(p,alt_ini)
   # alt_ini = consumidor_cupom(p,alt_ini)
    alt_ini = subtotal_mov_caixa(p,alt_ini)
    alt_ini = porcentagem_caixa(p,alt_ini)
    alt_ini = observacoes_caixa(p,alt_ini)
    alt_ini = total_geral(p,alt_ini)
    alt_ini = rodape_caixa(p,alt_ini)

    p.setPageSize((7.9*cm,(alt_ini/28)*cm)) # Utilizado para alterar o tamanho da página antes da impressão
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer,as_attachment=False,filename=f'movimento_caixa.pdf')
#mov_caixa geral 

def mov_caixa(request, pk):
    print("teste19")
    # Variáveis
    alt_ini = 55
    tf = 7 # Tamanho da fonte
    pl = 8 # Pulo de linha

    # Consultas ao banco de dados
    data = datetime
    #venda = get_object_or_404(Venda, pk = pk)
    mov_caixa=get_object_or_404(Mov_caixa,pk=pk)
    
   # user = get_object_or_404(User,pk=request.User.id)
    setor= get_object_or_404(Setor,pk=mov_caixa.cod_seto_mov_c.key_setor)
    # Verifica se é Cupom Fiscal de Consumidor Eletrônica (65) ou Nota Fiscal Eletrônica
    #if request.method == 'GET' and int(venda.modelo_nf_ven) != 65:
    #    messages.warning(request,'Nota Fiscal de Consumidor Eletrônica só pode ser emitida para Modelo NF igual a 65. (Escolha um modelo válido: 55 - NFe, 65 - NFCe)')
    #    return redirect('core:detalhe_venda',pk)

    # Definições da página
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer,pagesize=(7.9*cm,0*cm),bottomup=0,pageCompression=0,verbosity=0,)
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    pdfmetrics.registerFont(TTFont('ArialBd', 'ArialBd.ttf'))
    p.setFont("Arial",tf)    
    p.setTitle(f'Movimento de caixa _{mov_caixa.id_mov_Caixa}_{setor.desc_setor}')

    p.drawImage('./vendas/core/static/img/logo_cabecalho.bmp',62.5,5,width=100,height=50,preserveAspectRatio=True,mask=None)

    def cabecalho_mov(self,alt_ini):
        setor = Setor.objects.get(pk=mov_caixa.cod_seto_mov_c.key_setor)
        titulos = 0
        mome_cad="nome_cad"
        movimento =00000
        esp = 0000
        p.drawCentredString(224/2, alt_ini+pl, f'MOVIMENTO DE CAIXA:{mov_caixa.data_mov} {mov_caixa.id_mov_Caixa}')
       # p.drawCentredString(224/2, alt_ini+pl, f'empresaVenda.razao_ca - Fone: empresaVenda.telefone1_cad')
        #p.drawCentredString(224/2, alt_ini+pl*2, f'CNPJ: empresaVenda.cgc_cpf_cad - EI: empresaVenda.ie_cad')
        #p.drawCentredString(224/2, alt_ini+pl*3, f'empresaVenda.rua1_cad - empresaVenda.bairro1_cad')
        #p.drawCentredString(224/2, alt_ini+pl*5, f'Setor: {setor.key_setor} titulos:{formataValor(titulos)}')
        #p.drawCentredString(224/2, alt_ini+pl*6, f'nome_cadastro:TESTE  movimentos:{formataValor(movimento)}')
        #p.drawCentredString(224/2, alt_ini+pl*7, f'esp{formataValor(esp)} Entradas  Saidas')
        p.line(0,alt_ini+pl*2,224,alt_ini+pl*2)
        p.setFont('Arial',tf)
        p.line(0,alt_ini+pl*4,224,alt_ini+pl*4)
        p.drawString(9,alt_ini+pl*5,f'setor:{setor.key_setor} ')
        p.drawString(79,alt_ini+pl*5,f'titulos:{titulos}' )
        p.drawString(150,alt_ini+pl*5,'nome_cad:')
        print(mov_caixa.Troco_inicial)
        p.drawString(9,alt_ini+pl*6,'movimento')
        p.drawString(79,alt_ini+pl*6,'esp')
        p.line(0,alt_ini+pl*7,224,alt_ini+pl*7)
        return alt_ini+pl*8

    def cupom_dados(self,alt_ini):
              
       # p.drawString(9,alt_ini,f'{setor.key_setoro}')
       # p.drawString(79,alt_ini,f'{formataValor(titulos)}')            
       # p.drawString(45,alt_ini+pl,f'{nome_cad}')
       # p.drawString(93,alt_ini+pl,f'{formataValor(movimento)}')
       # p.drawRightString(215,alt_ini+pl,f'{formataValor(esp)}')
        alt_ini += pl*2
        #p.line(0,alt_ini-pl*0.5,224,alt_ini-pl*0.5)
       # p.drawString(9,alt_ini+pl*0.5,f'QTD. TOTAL DE ITENS')
       # p.drawRightString(215,alt_ini+pl*0.5,f'{qtd_total_itens}')
        print("teste20")
        return alt_ini + pl*2
    def resumo_impressao_caixa(self,alt_ini):
        print("teste20")
        #valor_produtos = 0
        #for i in range(itens.count()):
        #    produto = Produto.objects.get(produto_pro=itens[i].produto_ite_id)
        #    valor_produtos += itens[i].quantidade_ite * itens[i].unitario_ite
        p.drawString(9,alt_ini,'A vista ')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl,'Boleto Bancario')
        p.drawRightString(200,alt_ini+pl,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,'Contra Apres.')
        p.drawRightString(200,alt_ini+pl*2,f'{formataValor(0)}')
        p.drawString(9,alt_ini,'Cheque pré')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl,'Carteira')
        p.drawRightString(200,alt_ini+pl,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,'cheque pre datado')
        p.drawRightString(200,alt_ini+pl*2,f'{formataValor(0)}')
        p.drawString(9,alt_ini,'Convenio')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl,'Cartao')
        p.drawRightString(200,alt_ini+pl,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,'Troco inicial')
        p.drawRightString(215,alt_ini+pl*2,f'{formataValor(mov_caixa.Troco_inicial)}')
        p.drawString(9,alt_ini,'Vendasa vista')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl,'dv+ tk clientes (-)')
        p.drawRightString(200,alt_ini+pl,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,'np+ca+ct')
        p.drawRightString(200,alt_ini+pl*2,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*3,'Saidas(-) (- Dv+Tr)')
        p.drawRightString(200,alt_ini+pl*3,f'{formataValor((0))}%')
        p.drawRightString(200,alt_ini+pl*3,f'{formataValor((0))}%')
        alt_ini += pl*4.5
        p.drawString(9,alt_ini,'suprimento -cheques')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
       # p.drawString(9,alt_ini+pl,f'{condicao.descricao if venda.condicao_ven != None else "Dinheiro"}')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,f'TRansf - Entradas')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,f'Nota Fiscal')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,f'Nota Promissória')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,f'- Vale')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,f'Convênio')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,f'Outros')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.line(0,alt_ini+pl*2.5,224,alt_ini+pl*2.5)
        p.drawRightString(200,alt_ini+pl*4,f'{formataValor(mov_caixa.Troco_inicial)}')
        print("teste21")
        return alt_ini + pl*5#
    def subtotal_mov_caixa (self,alt_ini):
        print("teste20")
        soma_tudo = 0
        print(soma_tudo)
        p.drawString(9,alt_ini,'A - A vista ')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl,'B - Boleto Bancario')
        p.drawRightString(200,alt_ini+pl,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,'C - Contra Apres.')
        p.drawRightString(200,alt_ini+pl*2,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*3,'D - Cheque pré')
        p.drawRightString(200,alt_ini+pl*3,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*4,'E - Carteira')
        p.drawRightString(200,alt_ini+pl*4,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*5,'F - Duplicada')
        p.drawRightString(200,alt_ini+pl*5,f'{formataValor(0)}')
        p.line(0,alt_ini+pl*6,224,alt_ini+pl*6)
        p.drawString(9,alt_ini+pl*7,'G - Nota Fiscal')
        p.drawRightString(200,alt_ini+pl*7,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*8,'H - Nota Promissória')
        p.drawRightString(200,alt_ini+pl*8,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*9,'I  - Vale .')
        p.drawRightString(200,alt_ini+pl*9,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*10,'J - Cartão-pix')
        p.drawRightString(200,alt_ini+pl*10,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*11,'K - convenio')
        p.drawRightString(200,alt_ini+pl*11,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*12,'L - Outros(RP,XX,CX)')
        p.drawRightString(200,alt_ini+pl*12,f'{formataValor(0)}')
        p.line(0,alt_ini+pl*13,224,alt_ini+pl*13)
        p.drawString(9,alt_ini+pl*14,'Cheque pre datado')
        p.drawRightString(200,alt_ini+pl*14,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*15,'Convenio')
        p.drawRightString(200,alt_ini+pl*15,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*16,'Cartao')
        p.drawRightString(200,alt_ini+pl*16,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*17,'Troco inicial')
        p.drawRightString(200,alt_ini+pl*17,f'{formataValor(mov_caixa.Troco_inicial)}')
        p.drawString(9,alt_ini+pl*18,'Vendasa vista')
        p.drawRightString(200,alt_ini+pl*18,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*19,'DV+ TK clientes (-)')
        p.drawRightString(200,alt_ini+pl*19,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*20,'NP+CA+CT')
        p.drawRightString(200,alt_ini+pl*20,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*21,'Saidas(-) (- Dv+Tr)')
        p.drawRightString(200,alt_ini+pl*21,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*22,'suprimentos-cheques')
        p.drawRightString(200,alt_ini+pl*22,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*23,'suprimentos-dinheiro')
        p.drawRightString(200,alt_ini+pl*23,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*24,'Sangria/Retirada')
        p.drawRightString(200,alt_ini+pl*24,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*25,'TRanst-entradas')
        p.drawRightString(200,alt_ini+pl*25,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*26,'Transt-saidas')
        p.drawRightString(200,alt_ini+pl*26,f'{formataValor(0)}')
        #p.drawString(9,alt_ini+pl,f'{condicao.descricao if venda.condicao_ven != None else "Dinheiro"}')
        #p.drawRightString(9,alt_ini*15,f'Sangria/Retirada (-)')
       # p.drawRightString(215,alt_ini+pl*15,f'{formataValor((0))}')
        #p.drawString(9,alt_ini+pl*16,f'TRansf - Entradas')
        #p.drawRightString(215,alt_ini+pl*16,f'{formataValor((0))}')
        #p.drawRightString(9,alt_ini*17,f'tans-saidas')
        #p.drawRightString(215,alt_ini+pl*17,f'{formataValor((0))}')
        #p.drawString(9,alt_ini*18,f'Caixa FInal')
        #Modificado (retirado + venda.acrescimo_ven) Rennan 03/05/2022
        #modificado(retirado venda.desconto) Davi O 03/05/2022
        #p.drawRightString(210,alt_ini+pl*18,f'{formataValor(0)}')#venda.desconto_ven)}')
        p.line(0,alt_ini+pl*28,224,alt_ini+pl*28)
        #p.drawString(7,alt_ini+pl*5.5,'Data do Vencimento')
        #p.drawRightString(210,alt_ini+pl*5.5,'Valor do Pagamento')
        #p.drawString(7,alt_ini+pl*6.5,f'{mov_caixa.get_data_ven()}')
        #Modificado (retirado + venda.acrescimo_ven) Rennan 03/05/2022
        # modificado(retirado venda.desconto) Davi O 03/05/2022
        p.drawString(9,alt_ini+pl*29,'Caixa Final')
        p.drawRightString(210,alt_ini+pl*29,f'{formataValor((soma_tudo) +mov_caixa.Troco_inicial   )}')#venda.desconto_ven#)}')
        p.line(0,alt_ini+pl*30,224,alt_ini+pl*30)
        print("teste23")
        return alt_ini+pl*32  

    #def itens_cupom(self,alt_ini):
    #    produto = ''
    #    cont = 1
    #    p.drawString(7,alt_ini,'titulos baixados ')
    #    p.drawString(35,alt_ini,'CODIGO')
    #    p.drawString(115,alt_ini,'DESCRICAO')
    #    p.drawString(45,alt_ini+pl,'UN.')
    #    p.drawString(70,alt_ini+pl,'PR.UNIT.')
    #    p.drawRightString(210,alt_ini+pl,'PRECO TOTAL')
    #    for i in range(itens.count()):
    #        produto = Produto.objects.get(produto_pro=itens[i].produto_ite_id)
    #        cont += 1
    #        p.drawString(7,alt_ini+(pl*cont),f'{i+1}')
    #        p.drawString(40,alt_ini+(pl*cont),f'{produto.produto_pro}')
    #        p.drawString(70,alt_ini+(pl*cont),f'{produto.descricao_pro[0:40]}')
    #        cont += 1
    #        p.drawString(21,alt_ini+(pl*cont),f'{itens[i].quantidade_ite}')
    #        p.drawString(45,alt_ini+(pl*cont),f'{produto.unidade_pro}')
    #        p.drawString(70,alt_ini+(pl*cont),f'{formataValor(itens[i].unitario_ite)}')
    #        p.drawString(115,alt_ini+(pl*cont),f'TOTAL:')
    #        p.drawRightString(210,alt_ini+(pl*cont),f'{formataValor(itens[i].quantidade_ite * itens[i].unitario_ite)}')
    #    cont += 1
    #    p.drawString(7,alt_ini+(pl*cont),f'---Localiz.:{123} Sigla:{132}')
    #    return alt_ini+pl*(cont+2)

    #def consumidor_cupom(self,alt_ini):
    #    p.drawString(7,alt_ini,f'MINAS LEGAL 039134040803202296')
    #    p.drawString(7,alt_ini+pl,f'{cliente.nome_cad}')
    #    p.drawString(7,alt_ini+pl*2,f'{cliente.rua1_cad}')
    #    p.drawString(7,alt_ini+pl*3,f'BRASIL')
    #    p.drawString(100,alt_ini+pl*3,f'{cliente.cidade1_cad}-{cliente.estado1_cad}')
    #    p.line(0,alt_ini+pl*3.5,224,alt_ini+pl*3.5)
    #    return alt_ini+pl*4.5
        
    def subtotal_mov_caixa (self,alt_ini):
        print("teste20")
        soma_tudo = 0
        print(soma_tudo)
        p.drawString(9,alt_ini,'A - A vista ')
        p.drawRightString(200,alt_ini,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl,'B - Boleto Bancario')
        p.drawRightString(200,alt_ini+pl,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*2,'C - Contra Apres.')
        p.drawRightString(200,alt_ini+pl*2,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*3,'D - Cheque pré')
        p.drawRightString(200,alt_ini+pl*3,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*4,'E - Carteira')
        p.drawRightString(200,alt_ini+pl*4,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*5,'F - Duplicada')
        p.drawRightString(200,alt_ini+pl*5,f'{formataValor(0)}')
        p.line(0,alt_ini+pl*6,224,alt_ini+pl*6)
        p.drawString(9,alt_ini+pl*7,'G - Nota Fiscal')
        p.drawRightString(200,alt_ini+pl*7,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*8,'H - Nota Promissória')
        p.drawRightString(200,alt_ini+pl*8,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*9,'I  - Vale .')
        p.drawRightString(200,alt_ini+pl*9,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*10,'J - Cartão-pix')
        p.drawRightString(200,alt_ini+pl*10,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*11,'K - convenio')
        p.drawRightString(200,alt_ini+pl*11,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*12,'L - Outros(RP,XX,CX)')
        p.drawRightString(200,alt_ini+pl*12,f'{formataValor(0)}')
        p.line(0,alt_ini+pl*13,224,alt_ini+pl*13)
        p.drawString(9,alt_ini+pl*14,'Cheque pre datado')
        p.drawRightString(200,alt_ini+pl*14,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*15,'Convenio')
        p.drawRightString(200,alt_ini+pl*15,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*16,'Cartao')
        p.drawRightString(200,alt_ini+pl*16,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*17,'Troco inicial')
        p.drawRightString(200,alt_ini+pl*17,f'{formataValor(mov_caixa.Troco_inicial)}')
        p.drawString(9,alt_ini+pl*18,'Vendasa vista')
        p.drawRightString(200,alt_ini+pl*18,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*19,'DV+ TK clientes (-)')
        p.drawRightString(200,alt_ini+pl*19,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*20,'NP+CA+CT')
        p.drawRightString(200,alt_ini+pl*20,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*21,'Saidas(-) (- Dv+Tr)')
        p.drawRightString(200,alt_ini+pl*21,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*22,'suprimentos-cheques')
        p.drawRightString(200,alt_ini+pl*22,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*23,'suprimentos-dinheiro')
        p.drawRightString(200,alt_ini+pl*23,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*24,'Sangria/Retirada')
        p.drawRightString(200,alt_ini+pl*24,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*25,'TRanst-entradas')
        p.drawRightString(200,alt_ini+pl*25,f'{formataValor(0)}')
        p.drawString(9,alt_ini+pl*26,'Transt-saidas')
        p.drawRightString(200,alt_ini+pl*26,f'{formataValor(0)}')
        #p.drawString(9,alt_ini+pl,f'{condicao.descricao if venda.condicao_ven != None else "Dinheiro"}')
        #p.drawRightString(9,alt_ini*15,f'Sangria/Retirada (-)')
       # p.drawRightString(215,alt_ini+pl*15,f'{formataValor((0))}')
        #p.drawString(9,alt_ini+pl*16,f'TRansf - Entradas')
        #p.drawRightString(215,alt_ini+pl*16,f'{formataValor((0))}')
        #p.drawRightString(9,alt_ini*17,f'tans-saidas')
        #p.drawRightString(215,alt_ini+pl*17,f'{formataValor((0))}')
        #p.drawString(9,alt_ini*18,f'Caixa FInal')
        #Modificado (retirado + venda.acrescimo_ven) Rennan 03/05/2022
        #modificado(retirado venda.desconto) Davi O 03/05/2022
        #p.drawRightString(210,alt_ini+pl*18,f'{formataValor(0)}')#venda.desconto_ven)}')
        p.line(0,alt_ini+pl*28,224,alt_ini+pl*28)
        #p.drawString(7,alt_ini+pl*5.5,'Data do Vencimento')
        #p.drawRightString(210,alt_ini+pl*5.5,'Valor do Pagamento')
        #p.drawString(7,alt_ini+pl*6.5,f'{mov_caixa.get_data_ven()}')
        #Modificado (retirado + venda.acrescimo_ven) Rennan 03/05/2022
        # modificado(retirado venda.desconto) Davi O 03/05/2022
        p.drawString(9,alt_ini+pl*29,'Caixa Final')
        p.drawRightString(210,alt_ini+pl*29,f'{formataValor((soma_tudo) +mov_caixa.Troco_inicial   )}')#venda.desconto_ven#)}')
        p.line(0,alt_ini+pl*30,224,alt_ini+pl*30)
        print("teste23")
        return alt_ini+pl*32  

    def itens_MOVCAIXA(self,alt_ini):
        produto = ''
        cont = 1
        p.drawString(9,alt_ini,'titulos baixados ')    
        p.drawString(9,alt_ini+pl,'numero de vendas ')
        p.line(1.5,alt_ini+pl*1.5,224,alt_ini+pl*1.5)
        p.drawString(9,alt_ini+pl*2.5,'saidas ')
        p.drawString(9,alt_ini+pl*3.5,'entradas')


        #p.drawString(70,alt_ini+pl,'PR.UNIT.')
        #p.drawRightString(210,alt_ini+pl,'PRECO TOTAL')
        #for i in range(vendas.count()):
        #    produto = Produto.objects.get(produto_pro=itens[i].produto_ite_id)
        #    cont += 1
        #    p.drawString(7,alt_ini+(pl*cont),f'{i+1}')
        #    p.drawString(40,alt_ini+(pl*cont),f'{formatavalor (0)}')
            #p.drawString(70,alt_ini+(pl*cont),f'{produto.descricao_pro[0:40]}')
        #    cont += 1
            #p.drawString(21,alt_ini+(pl*cont),f'{caixa_ven}')
            #p.drawString(45,alt_ini+(pl*cont),f'{produto.unidade_pro}')
            #p.drawString(70,alt_ini+(pl*cont),f'{formataValor(itens[i].unitario_ite)}')
            #p.drawString(115,alt_ini+(pl*cont),f'TOTAL:')
           # p.drawRightString(210,alt_ini+(pl*cont),f'{formataValor(itens[i].quantidade_ite * itens[i].unitario_ite)}')
        #cont += 1
        p.drawString(100,alt_ini+(pl*3),f'---Localiz.:{123} Sigla:{132}')
        p.line(0,alt_ini+pl*4,224,alt_ini+pl*4)
        return alt_ini+pl*(cont+4)
    def porcentagem_caixa(self,alt_ini):
        

        p.drawString(9,alt_ini+pl,f'produtos a vista')
        p.drawRightString(200,alt_ini+pl,f'{formataValor((0))+"---"+formataPorcent((0))}')
        p.drawString(9,alt_ini+pl*2,f'servicos a vista')
        p.drawRightString(200,alt_ini+pl*2,f'{formataValor((0))+"---"+formataPorcent((0))}')
        p.drawString(9,alt_ini+pl*3,f'produtos a praso')
        p.drawRightString(200,alt_ini+pl*3,f'{formataValor((0))+"---"+formataPorcent((0))}')
        p.drawString(9,alt_ini+pl*4,f'servico a praso')
        p.drawRightString(200,alt_ini+pl*4,f'{formataValor((0))+"---"+formataPorcent((0))}')
        p.line(0,alt_ini+pl*5,224,alt_ini+pl*5)
        return alt_ini + pl* 6
    def caixa_final(self, alt_ini):
        p.drawString(9,alt_ini+pl*2,f'caixa final')
        p.drawRightString(200,alt_ini+pl*3,f'{formataValor((0))}')
        p.drawString(9,alt_ini+pl*2,f'diferencial de caixa ')
        p.drawRightString(200,alt_ini+pl*3,f'{formataValor((0))}')
        print("teste25")    
        return alt_ini + pl*5
    



    def observacoes_caixa (self,alt_ini):
        p.drawString(7,alt_ini,'OBSERVAÇÕES:')
       # count = len(venda.obs_ven) / 40 if venda.obs_ven != None else 0
       # if count > 1:
       #     parada = 0
       #     i = 0
       #     while i < count:
       #         if i > 5:
       #             break
       #         p.drawString(7,alt_ini+(pl*(i+1)),f'{venda.obs_ven[parada:parada+40]}')
       #         i += 1
       #         parada += 40
        #else:            
        #p.drawString(7,alt_ini+pl,f'{venda.obs_ven if venda.obs_ven != None else ""}')
        p.drawString(152,alt_ini+pl*7,'Versão:1.0')
        p.line(0,alt_ini+pl*6.7,150,alt_ini+pl*6.7)
        p.line(0,alt_ini+pl*6.8,150,alt_ini+pl*6.8)
        p.line(193,alt_ini+pl*6.7,224,alt_ini+pl*6.7)
        p.line(193,alt_ini+pl*6.8,224,alt_ini+pl*6.8)
        print("teste26")
        return alt_ini+pl*8
    def total_geral (self,alt_ini):
        p.drawString(9,alt_ini+pl,f'valor total ')
        p.drawRightString(200,alt_ini+pl,f'{formataValor((0))}')
        p.drawString(9,alt_ini+pl*2,'saldo anterior')
        p.drawRightString(200,alt_ini+pl*2,f'{formataValor((0))}')
        print("teste27")
        p.line(0,alt_ini+pl*3,224,alt_ini+pl*3)
        return alt_ini+pl*4
    def rodape_caixa(self,alt_ini):
        #p.drawCentredString(224/2,alt_ini,'Não é Documento Fiscal')
        p.drawCentredString(224/2,alt_ini+pl,'MOVIMENTO DE CAIXA ')
        p.drawString(78,alt_ini+pl*2,f'{datetime.today().strftime("%d/%m/%Y")} {datetime.today().strftime("%H:%M:%S")}')
        return alt_ini+pl*7

    alt_ini = cabecalho_mov(p,alt_ini)
    alt_ini = itens_MOVCAIXA(p,alt_ini)
   # alt_ini = consumidor_cupom(p,alt_ini)
    alt_ini = subtotal_mov_caixa(p,alt_ini)
    alt_ini = porcentagem_caixa(p,alt_ini)
    alt_ini = observacoes_caixa(p,alt_ini)
    alt_ini = total_geral(p,alt_ini)
    alt_ini = rodape_caixa(p,alt_ini)

    p.setPageSize((7.9*cm,(alt_ini/28)*cm)) # Utilizado para alterar o tamanho da página antes da impressão
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer,as_attachment=False,filename=f'movimento_{mov_caixa.id_mov_Caixa}.pdf')
